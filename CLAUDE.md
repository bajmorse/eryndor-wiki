# Eryndor Repository Instructions

## Purpose

This repository contains the canonical lore, worldbuilding, history, geography, cultures, politics, economics, cosmology, and game content for the fantasy setting of Eryndor.

All files within this repository should be treated as the source of truth for the setting.

When creating or modifying lore, prioritize consistency with existing articles over generating new ideas.

---

# Primary Lore Sources

The world encyclopedia located at:

info/encyclopedia.md

contains the current canonical history, cosmology, races, continents, institutions, economics, politics, and major historical figures of Eryndor.

When creating new lore:

1. Maps
2. info/encyclopedia.md
3. Existing repository articles
4. Repository instructions
5. Newly generated content

The encyclopedia should be treated as the primary lore reference unless a more specific article explicitly overrides it.

---

# Core World Principles

## Climate

Unlike Earth:

* The north is warmer.
* The south is colder.

This affects all geography, cultures, ecosystems, migration patterns, agriculture, trade, and settlement.

Examples:

* Velkrand's volcanic regions exist in the northwestern portions of the world.
* Hrothan is the frozen southern continent.
* Tropical islands are generally found farther north.

---

# Cosmology

The setting uses a layered cosmology consisting of:

* The Hallows Above
* The Mortal Plane
* The Circles Below
* The Realms Beyond

The Realms Beyond include:

* The Astral Plane
* The Elemental Realms
* The Void

The Celestial War, the Shattering, Khael, Gontkhael, Nythorak, Angels, Devils, Dragons, Demons, and the origins of mortal life are described in detail within:

info/encyclopedia.md

and should be treated as canonical.

---

# Modern Dating

The current year is approximately:

**300 AU**

Where:

* AU = After Unification
* BU = Before Unification

The Unification marks:

* The sealing of the Void Rift
* Peace between Mortals and Demons
* The beginning of the Modern Age

---

# Major Regions

## Eldressa

The historical heart of civilization.

Key features:

* Largest center of population and political influence.
* Home of Rivara and Valtiron.
* Power is fragmented among many independent states.
* The Council convenes in Valtiron.
* Valtiron serves as the political heart of Eldressa.
* Rivara remains one of the world's most influential financial centers.

Modern Eldressa resembles a collection of nations, city-states, and regional powers rather than a unified empire.

---

## Velkrand

Industrial continent of forge-cities, free cities, miners, artificers, engineers, and maritime republics.

Key features:

* Curved, asymmetrical continent.
* Embercrown volcanic range dominates the north and northwest.
* Southern coast contains towering cliffs and airship ports.
* Interior contains mines, quarries, railways, and industrial settlements.
* Free cities retain varying degrees of autonomy.

The Velkrand Compact is gradually pushing the continent toward political and economic unification.

---

## Ilyndor

Primal wilderness continent.

Key features:

* New Zealand-inspired geography.
* No centralized government.
* Dominated by forests, plains, highlands, jungles, rivers, and rugged southern mountains.
* The Heartwood is the sacred center of the continent.
* Home of the Woodland Guardians.

The continent is inhabited by Deonati, Katari, Faeries, Fauns, Fungril, Galapa, Eladrin, and scattered frontier settlements.

The Woodland Guardians hold significant spiritual influence but do not directly govern the continent.

---

## Meridian Isles

Also known as the Freewaters.

Key features:

* Maritime crossroads of the world.
* Meridia is the diplomatic and economic center of the known world.
* Nadris is a major smuggler and free-captain port.
* Most islands remain wild, sparsely settled, or unexplored.
* Strong pirate, merchant, explorer, and adventurer culture.

No single government controls the archipelago.

---

## Skeldran

Shattered northern continent.

Key features:

* Massive fractured landmass.
* Surrounded by the Obsidian Reaches.
* Dense fog, dangerous seas, and black obsidian cliffs.
* Sparse settlements.
* Greywatch is the primary inhabited settlement.
* Civilization survives rather than thrives.
* Fossilized Leviathan remains dominate much of the landscape.

Skeldran was once stewarded by the Leviathans.

The continent was shattered during the Leviathan War long before the First Demon War.

Ancient peoples of Skeldran included:

* Selkari
* Tidemarked
* Corvani

Modern settlements are rare and most of the continent remains unexplored.

---

## Hrothan

Frozen southern homeland of humanity.

Key features:

* Vast tundra continent.
* Humanity originated here before migrating north.
* Home to Human tribes, Goliath clans, and Giant territories.
* Very few permanent settlements.
* Large frozen inland lake.
* Ancient migration routes marked by cairns and standing stones.
* No continent-wide government.

Hrothan should feel primordial and unforgiving rather than ruined or post-apocalyptic.

---

# Major World Institutions

## Council of Valtiron

Closest equivalent to an international diplomatic body.

* Convenes in Valtiron.
* Possesses influence but limited direct authority.
* Functions similarly to a mixture of the UN and EU.

---

## Rivara

One of the world's most influential financial centers.

Influence derives primarily from:

* Banking
* Trade
* Commerce
* Shipping
* Merchant houses

---

## Meridia

Diplomatic and economic capital of the known world.

Neutral territory where major powers meet.

Home of:

* The Bank of Unification
* Numerous trade houses
* International guilds
* Dragon rider embassies

---

## Bank of Unification

Primary financial institution of the known world.

* Headquartered in Meridia.
* Administers the Unified Crown.
* Maintains branches throughout the major continents.
* Operates the world's primary monetary system.

---

## Velkrand Compact

Growing industrial and political alliance attempting to unify Velkrand's independent powers.

---

## Heartwood

Spiritual center of Ilyndor.

Home of the Woodland Guardians.

---

## Dragon Riders

The principal communication and diplomatic network connecting the continents.

Established following the return of the Dragons during the Age of Reconnection.

---

# Writing Guidelines

## Tone

Maintain a high-fantasy tone.

Avoid:

* Excessive grimdark.
* Excessive comedy.
* Modern slang.
* Meta commentary.

---

## Worldbuilding Style

Prefer:

* Layered history.
* Cultural nuance.
* Political complexity.
* Economic realism.
* Regional identity.
* Geographic realism.

Avoid:

* Monocultures.
* Planet-of-hats civilizations.
* Generic fantasy tropes unless intentionally subverted.

---

## Settlements

Most settlements should emerge naturally from:

* Geography
* Trade
* Resources
* Defense
* Culture
* Religion
* Historical circumstance

Avoid creating cities without a clear reason to exist.

---

## Continuity

Never contradict established canon.

When uncertain:

1. Search existing articles.
2. Consult info/encyclopedia.md.
3. Expand existing lore.
4. Create new lore only when necessary.

---

# Repository Structure

## Public Lore

Located under:

content/

This content is intended for publication.

---

## GM-Only Lore

Located under:

gm/

Contains:

* Campaign secrets
* Storylines (current state, established truths, party knowledge, rumours, open questions, NPCs, related storylines, recent developments, consequences, uncommitted ideas)
* Session notes
* Future story arcs
* Hidden factions
* Villain plans
* Cosmological truths

This directory is built only into the private GM site (gm.eldressa.fyi). The player build never reads it — the player Docker image's build stage never copies gm/ into its filesystem, so this is a physical guarantee, not just an access-control one.

Never expose GM information in public (content/) articles without explicit instruction. GM pages may freely [[wikilink]] to content/ pages and to other gm/ pages.

---

# Maps

Maps are canonical.

When written lore conflicts with maps:

Maps take precedence.

Maintain consistency with established geography, scale, climate, and regional placement.

---

# Canon Hierarchy

Highest Priority:

1. Maps
2. info/encyclopedia.md
3. Existing repository articles
4. Repository instructions
5. Newly generated content

New content should always preserve established canon whenever possible.
