import cv2
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import shutil
from pathlib import Path
from skimage.morphology import skeletonize
from skimage import img_as_bool, img_as_ubyte
from scipy.spatial import ConvexHull
from scipy.ndimage import binary_dilation


def generate_output_names(image_path):
    """Generuje nazwy plików wyjściowych na podstawie ścieżki wejściowej."""
    base_path = os.path.splitext(image_path)[0]
    stars_json = f"{base_path}_stars.json"
    bbox_json = f"{base_path}_bbox.json"
    return stars_json, bbox_json

# ta funkcja zajebiscie rysuje nowe zdjecie ale bbox chujowo
def extract_constellation_data(image_path, constellation_name, output_dir):
    """
    Przetwarza obraz konstelacji, wykrywa gwiazdy i tworzy pliki treningowe dla YOLO.
    Ignoruje linie łączące gwiazdy.

    Args:
        image_path: Ścieżka do obrazu konstelacji z liniami.
        constellation_name: Nazwa konstelacji (będzie używana jako etykieta).
        output_dir: Katalog wyjściowy do zapisania przetworzonych danych.

    Returns:
        Słownik zawierający ścieżki do wygenerowanych plików i informacje o bounding boxie.
    """
    # Tworzenie katalogów wyjściowych
    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    # Wczytanie oryginalnego obrazu
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Błąd: Nie można wczytać obrazu {image_path}")
        return None



    # Konwersja do skali szarości
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Wykrywanie jasnych punktów (gwiazd)
    _, thresh_stars = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Usuwanie małych obiektów (np. szumu) i izolowanie gwiazd
    kernel = np.ones((3, 3), np.uint8)
    stars_cleaned = cv2.morphologyEx(thresh_stars, cv2.MORPH_OPEN, kernel)

    # Wykrywanie konturów gwiazd
    star_contours, _ = cv2.findContours(stars_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    stars = []
    for contour in star_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 1 <= w <= 20 and 1 <= h <= 20:  # Filtrujemy tylko małe obiekty (gwiazdy)
            cx = x + w // 2
            cy = y + h // 2
            stars.append((cx, cy))

    if not stars:
        print(f"Nie znaleziono gwiazd w obrazie {image_path}")
        return None

    # Tworzenie obrazu z samymi gwiazdami (bez linii)
    stars_only_image = np.zeros_like(original_image)
    for cx, cy in stars:
        cv2.circle(stars_only_image, (cx, cy), 3, (255, 255, 255), -1)

    # Zapisanie obrazu z samymi gwiazdami
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    stars_only_path = os.path.join(images_dir, f"{base_name}_stars_only.jpg")
    cv2.imwrite(stars_only_path, stars_only_image)

    # Obliczanie bounding boxa dla wszystkich gwiazd
    coords = np.array(stars)
    x_min = np.min(coords[:, 0])
    y_min = np.min(coords[:, 1])
    x_max = np.max(coords[:, 0])
    y_max = np.max(coords[:, 1])

    # Dodanie marginesu do bounding boxa
    margin_x = (x_max - x_min) * 0.1
    margin_y = (y_max - y_min) * 0.1
    x_min = max(0, x_min - margin_x)
    y_min = max(0, y_min - margin_y)

    original_h, original_w = original_image.shape[:2]

    x_max = min(original_w - 1, x_max + margin_x)
    y_max = min(original_h - 1, y_max + margin_y)

    # Przygotowanie pliku adnotacji w formacie YOLO
    class_id = 0  # Możesz przypisać odpowiedni identyfikator klasy dla konstelacji
    x_center = ((x_min + x_max) / 2) / original_w
    y_center = ((y_min + y_max) / 2) / original_h
    width = (x_max - x_min) / original_w
    height = (y_max - y_min) / original_h

    label_path = os.path.join(labels_dir, f"{base_name}.txt")
    with open(label_path, 'w') as f:
        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    result = {
        'original_image': image_path,
        'stars_only_image': stars_only_path,
        'label': label_path,
        'num_stars': len(stars),
        'bbox': [x_min, y_min, x_max, y_max]
    }

    return result




def create_yolo_dataset(input_dir, output_dir, class_names=None):
    """
    Tworzy kompletny zestaw danych dla YOLO na podstawie przetworzonych obrazów.

    Args:
        input_dir: Katalog zawierający obrazy konstelacji
        output_dir: Katalog wyjściowy dla zestawu danych YOLO
        class_names: Lista nazw klas (konstelacji)
    """
    if class_names is None:
        class_names = ['constellation']

    dataset_dir = Path(output_dir)
    (dataset_dir / 'images' / 'train').mkdir(parents=True, exist_ok=True)
    (dataset_dir / 'images' / 'val').mkdir(parents=True, exist_ok=True)
    (dataset_dir / 'labels' / 'train').mkdir(parents=True, exist_ok=True)
    (dataset_dir / 'labels' / 'val').mkdir(parents=True, exist_ok=True)

    processed_data = []

    for constellation_dir in os.listdir(input_dir):
        constellation_path = os.path.join(input_dir, constellation_dir)
        if os.path.isdir(constellation_path):
            constellation_name = constellation_dir

            if constellation_name in class_names:
                class_id = class_names.index(constellation_name)
            else:
                class_names.append(constellation_name)
                class_id = len(class_names) - 1

            for img_file in os.listdir(constellation_path):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(constellation_path, img_file)
                    result = extract_constellation_data(
                        img_path,
                        constellation_name,
                        os.path.join(output_dir, 'temp', constellation_name)
                    )

                    if result:
                        result['class_id'] = class_id
                        processed_data.append(result)

    np.random.shuffle(processed_data)
    split_idx = int(len(processed_data) * 0.8)
    train_data = processed_data[:split_idx]
    val_data = processed_data[split_idx:]

    for idx, data in enumerate(train_data):
        stars_only_src = data['stars_only_image']
        stars_only_dst = dataset_dir / 'images' / 'train' / f"train_{idx}.jpg"
        shutil.copy2(stars_only_src, stars_only_dst)

        label_src = data['stars_only_label']
        label_dst = dataset_dir / 'labels' / 'train' / f"train_{idx}.txt"

        with open(label_src, 'r') as f_src:
            label_content = f_src.read()

        parts = label_content.split()
        if len(parts) >= 5:
            parts[0] = str(data['class_id'])
            new_label_content = ' '.join(parts)

            with open(label_dst, 'w') as f_dst:
                f_dst.write(new_label_content)

    for idx, data in enumerate(val_data):
        stars_only_src = data['stars_only_image']
        stars_only_dst = dataset_dir / 'images' / 'val' / f"val_{idx}.jpg"
        shutil.copy2(stars_only_src, stars_only_dst)

        label_src = data['stars_only_label']
        label_dst = dataset_dir / 'labels' / 'val' / f"val_{idx}.txt"

        with open(label_src, 'r') as f_src:
            label_content = f_src.read()

        parts = label_content.split()
        if len(parts) >= 5:
            parts[0] = str(data['class_id'])
            new_label_content = ' '.join(parts)

            with open(label_dst, 'w') as f_dst:
                f_dst.write(new_label_content)

    with open(dataset_dir / 'dataset.yaml', 'w') as f:
        f.write(f"# YOLOv10 dataset configuration\n")
        f.write(f"path: {os.path.abspath(dataset_dir)}\n")
        f.write(f"train: images/train\n")
        f.write(f"val: images/val\n")
        f.write(f"nc: {len(class_names)}\n")
        f.write(f"names: {class_names}\n")

    print(f"Utworzono zestaw danych YOLO w {dataset_dir}")
    print(f"Liczba obrazów treningowych: {len(train_data)}")
    print(f"Liczba obrazów walidacyjnych: {len(val_data)}")
    print(f"Liczba klas: {len(class_names)}")
    print(f"Klasy: {class_names}")

    return {
        'dataset_path': dataset_dir,
        'train_size': len(train_data),
        'val_size': len(val_data),
        'classes': class_names
    }


def main():

    input_dir = "dataset/raw_constellations"
    output_dir = "dataset/yolo_constellations"

    constellations = [
        "Andromeda", "Aquarius", "Aquila", "Aries",
        "Cancer", "CanisMinor", "Capricornus", "Cassiopeia",
        "Cygnus", "Gemini", "Leo", "Libra", "Orion",
        "Pegasus", "Perseus", "Pisces", "Sagittarius",
        "Scorpius", "Taurus", "UrsaMajor", "UrsaMinor", "Virgo"
    ]

    result = create_yolo_dataset(input_dir, output_dir, constellations)

    print("\nZakończono przygotowanie danych.")
    print(f"Zestaw danych gotowy do treningu YOLOv10: {result['dataset_path']}")


def test_single_image(image_path, output_dir="test_output"):
    """
    Testuje algorytm ekstrakcji na pojedynczym obrazie i wyświetla wyniki.
    """
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.basename(image_path)
    constellation_name = os.path.splitext(base_name)[0]

    result = extract_constellation_data(image_path, constellation_name, output_dir)

    if result:
        print(f"Przetestowano ekstrakcję dla: {constellation_name}")
        print(f"Wykryto {result['num_stars']} gwiazd")
        print(f"Bounding box: {result['bbox']}")
        print(f"Obraz z bounding boxem: {result['debug_image']}")

        debug_img = cv2.imread(result['debug_image'])
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(debug_img, cv2.COLOR_BGR2RGB))
        plt.title(f"Konstelacja: {constellation_name}")
        plt.axis('off')
        plt.show()
    else:
        print(f"Nie udało się przetworzyć obrazu: {image_path}")


if __name__ == "__main__":
    main()