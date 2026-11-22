# Foil demo page

Demo page for Foil, a self-play model for Magic: The Gathering (Standard). One static HTML file: a recorded game against a language model with a step slider, and a live game against the model.

## Build

    python build.py

Writes `index.html`. Python 3, no dependencies.

| File | Contents |
|---|---|
| `template.html` | Markup, styles, scripts |
| `game.json` | Recorded game: decisions, options, model probabilities |
| `lists.json` | Decklists for the deck picker, by archetype |

The live game calls `POST /v1/decide` on the page's own origin. Set `FOIL_API` to use another host:

    FOIL_API=https://host python build.py

## API

`POST /v1/decide`, JSON body:

| Field | Meaning |
|---|---|
| `decks` | Two decks in seat order: `{"list": "4 Card Name\n..."}` or a preset id |
| `seed` | Shuffle seed; seed + choices determine the game |
| `choices` | Option indexes chosen so far |
| `model_seats` | Seats the model plays, e.g. `[1]` |
| `format` | `"json"` or `"text"` |

Returns the acting player's view, the legal options with the model's probabilities, and its win estimate.

Magic: The Gathering is a trademark of Wizards of the Coast. This project is not affiliated with or endorsed by them.
