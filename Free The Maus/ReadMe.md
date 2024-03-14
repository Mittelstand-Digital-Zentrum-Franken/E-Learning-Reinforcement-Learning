# Free The Maus - Verloren im Labyrinth

Hier finden Sie die Beispiellösung für die Implementierung des Beispiels `Free The Maus - Verloren im Labyrinth`.

## Code Verzeichnis

- `QTable.py`: Hier ist es eine einfache Implementierung für eine mehrdimensionale Q-Table.
- `MazeEnvironment.py`: Hier ist eine Umgebung für das Labyrinth dargestellt.
- `MazeUtilities.py`: Hier gibt es verschiedene Hilfsfunktionen für das Laden und die Visualisierung von Labyrinthen.
- `Types.py`: Hier werden einige Datentypen definiert, die im restlichen Code benötigt werden.
- `QLearning.py`: Hier ist die beispielhafte Implementierung des Q-Learning-Algorithmus.

> &#9432; Am Ende jeder Datei finden Sie ein kleines Anwendungsbeispiel.

## Labyrinthen

Wir haben drei Beispiele für Labyrinthe in verschiedenen Größen. Natürlich können auch eigene Labyrinthe verwendet werden.

> Beispiel: 5x5 Labyrinth
>
>    ``` text
>    2, 0, 5, 0, 1;
>    1, 0, 4, 0, 1;
>    5, 0, 1, 4, 1;
>    0, 0, 0, 0, 0;
>    1, 1, 0, 1, 3;
>    ```
>
> Neue Zeilen werden mit `;` getrennt und Spalten mit `,`.
> Die einzelne Zustände werden wie folgt definiert:
>
> - 0:  Freie Position / Weiß
> - 1: Wand / Schwarz
> - 2: Maus / Blau
> - 3: Ausgang (Ziel) / Grün
> - 4: Käse (Neben Ziel) / Gelb
> - 5: Falle / Rot
