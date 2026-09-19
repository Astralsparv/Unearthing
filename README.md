# Unearthing (active development)

A text based mining game inspired by Stardew Valley and Steamworld Dig.

Designed for use with [More Perfect DOS VGA Font](https://laemeur.sdf.org/fonts/) (or stored locally at [MorePerfectDOSVGA.ttf](MorePerfectDOSVGA.ttf))and a 80x24 terminal.

## Controls

The game does not run in real-time, it only updates each time you input (by pressing enter).

You can choose to make no actions, or you can type in inputs.

### Directions

For moving around, this would be 'w','a','s' and 'd'.

Actions are made with the 'q' and 'e' key (see below).

If you don't type an action, you will simply move in the direction.

### Interactions

To mine or attack, you use 'q' and 'e', where 'q' is using your item and 'e' is interacting with a tile, e.g: using a ladder or picking up an item.

The item that will be used will be the currently selected one on your hotbar.

### Hotbar

The hotbar can be used to select different items with the left and right arrow key, where the tile surrounded in `<>` is the selected item.

## UI

### Map

On the left of the screen is the display of the map represented with text.

You can be seen on the map as the character `@`.

### Player Information

On the right, you will see your player information.

The first thing you will see is a view of what tile you are currently standing on (since it will be covered by the `@` symbol on the map).

For example:
```
...
.@.
...
```
when you're standing on the tile `.`


The rest of it is basic information such as your health, name and inventory.

The inventory is likely to be revamped to use a hotbar.
