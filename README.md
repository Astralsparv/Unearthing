# Unearthing (active development)

A text based mining game inspired by Stardew Valley and Steamworld Dig.

Designed for use with [More Perfect DOS VGA Font](https://laemeur.sdf.org/fonts/) (or stored locally at [MorePerfectDOSVGA.ttf](MorePerfectDOSVGA.ttf))and a 184x24 terminal

## Controls

The game does not run in real-time, it only updates each time you input (by pressing enter).

You can choose to make no actions, or you can type in inputs.

For moving around, this would be 'w','a','s' and 'd'.

For actions, you can interact with the tile you are on top of with 'e'.

### Mining and attacking

To mine or attack, you type two keys instead of one.

The first key is the direction (wasd), whilst the second key is 'q'.

Once a hotbar is implemented, it will be using your selected item (a weapon or a pickaxe), as of writing this; it is always the pickaxe (as no enemies are implemented).

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
