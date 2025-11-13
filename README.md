# Installation und Entwicklung

1. Erstelle eine virtuelle Python Umgebung mittels `python -m venv .venv`
2. Aktiviere die virtuelle Umgebung (Neustart des Terminals in VSCode, oder Ausführen von `.venv\Scripts\activate` unter Windows, oder Ausführen von `. .venv/bin/activate` unter Linux)
3. Installation der Abhängigkeiten und der Applikation selbst mittels `pip install -e .`
4. Start des Spiels durch Aufruf von `game` im Terminal

# Aufgaben
## Startscreen erweitern
* Der Titel "WDICGame" sollte zentriert angezeigt werden
* Darunter sollte stehen "Press Space to start."

## Begrenzung des linken Randes
* Im Moment wird das eigene Schiff durch den rechten Rand des Fensters begrenzt
* Das Schiff kann aber über den linken Rand hinaus fliegen -> dies sollte auch begrenzt werden

## Darstellungsänderung
Wenn eine Rakete abgefeuert wird, wird diese über das eigenen Schiffes gezeichnet. Die Rakete sollte aber unter des eigenen Schiffes gezeichnet werden.

## Graphiken hinzufügen
* Die Graphiken befinden sich im Verzeichnis `assets/images` - verwende die Funktion `get_asset_path` aus `utils`, um den korrekten Pfad zu erhalten 
* Verwende `images/enemy_ship.png` als Graphik für das gegnerische Schiff (`Enemy`)
* Verwende `images/player_missile.png` als Graphik für die eigenen abgefeuerten Raketen (`PlayerMissile`)
* Für das eigene Schiff (`Player`) wird bereits eine Graphik verwenden - verwende dies als Vorlage

## Sound hinzufügen
* Die Sounds befinden sich im Verzeichnis `assets/sounds` - verwende die Funktion `get_asset_path` aus `utils`, um den korrekten Pfad zu erhalten 
* Verwende `sounds/enemy_explosion.wav` als Sound für die Zerstörung eines gegnerische Schiffs
* Für das Abfeuern einer Rakete wird bereits ein Sound verwenden (in `Player.shoot`) - verwende dies als Vorlage

## Links/Rechts Steuerungslogik verbessern
Im Moment kommt es zu komischem Verhalten, wenn links und rechts teilweise gleichzeitig gedrückt bzw. losgelassen wird.

Beispiel:
1. Links drücken
2. Rechts drücken
3. Links loslassen

-> Das Schiff bleibt stehen, obwohl rechts gerade gedrückt wird.

## Punktestand
Das Objekt `Game` enthält einen Attribut für den Punktestand (`score`)

* Gestartet wird bei 0
* Abschuss eines Gegners gibt einen Punkt

Der Punktestand soll rechts oben angezeigt werden.

## Kollision mit dem Gegner
* In der dritten Welle kommen die Gegner bis ans untere Ende des Bildschirms und können dadurch mit dem Schiff kollidieren
* Bei einer Kollision soll ein "Game Over" Bildschirm angezeigt werden

## Weitere Ideen
* Hinzufügen von zusätzlichen Angriffswellen
* Textanzeige, wenn eine neue Angriffs-Welle startet
* Hinzufügen von gegnerischen Schiffen, die selbst feuern können
* Hinzufügen von "Leben"
* Hinzufügen von neuen "Raketentypen" (z.B. drei Raketen gleichzeitig)
* Hintergrundbild, welches während des Fluges von oben nach unten durchscrollt
* Dem Spieler die Möglichkeit geben, das Raumschiff auch nach oben/unten zu steuern
* ...

# Credits

* Bilder und Töne wurden verwendet von
  * [claudiu-codreanu/alien-invaders-v2](https://github.com/claudiu-codreanu/alien-invaders-v2/tree/main/asset)
  * [DanieloFleming/meteor-strike](https://github.com/DanieloFleming/meteor-strike/tree/master)
