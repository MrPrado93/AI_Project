from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# Ubica el archivo CSV junto a este script para poder ejecutarlo desde cualquier carpeta.
RUTA_PRODUCTOS = Path(__file__).with_name("products.csv")
CARACTERISTICAS = ["feature1", "feature2", "feature3"]


def recommend(
    modelo: KNeighborsClassifier,
    feature1: float,
    feature2: float,
    feature3: float,
) -> str:
    """Predice la categoría del producto a partir de sus tres características."""
    producto = pd.DataFrame(
        [[feature1, feature2, feature3]],
        columns=CARACTERISTICAS,
    )
    return str(modelo.predict(producto)[0])


def main() -> None:
    # Carga los productos y separa las características de la categoría objetivo.
    productos = pd.read_csv(RUTA_PRODUCTOS)
    X = productos[CARACTERISTICAS]
    y = productos["label"]

    # Conserva la proporción de categorías en los conjuntos de entrenamiento y prueba.
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # Entrena el clasificador con los tres vecinos más cercanos.
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X_entrenamiento, y_entrenamiento)

    # Evalúa el modelo con datos que no se usaron durante el entrenamiento.
    predicciones = modelo.predict(X_prueba)
    accuracy = accuracy_score(y_prueba, predicciones)
    print(f"Accuracy: {accuracy:.2%}")

    # Ejemplo: recomienda una categoría para un producto nuevo.
    categoria = recommend(modelo, feature1=2.5, feature2=10.5, feature3=101.0)
    print(f"Categoria recomendada para el producto de ejemplo: {categoria}")


if __name__ == "__main__":
    main()