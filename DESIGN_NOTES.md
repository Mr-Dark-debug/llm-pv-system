# Design Notes

## Scope

This project implements the operator prompt as a runnable FastAPI + SQLite + Jinja2 platform under the required `llm_pv_system/` layout.

## Ambiguities Resolved

- The attached prompt ends during section 5.8, so sections 6-16 were implemented from the visible table of contents and earlier requirements.
- The exact 90 benchmark prompts were not fully present in the attachment. The app seeds 90 standardized prompts across the required three prompt families: 30 context-free, 30 context-rich, and 30 metalinguistic prompts.
- The PHaVE master list itself was not included in the attachment. The app includes a PHaVE-inspired phrasal-verb master list with transparency labels and documents where to replace it with the licensed/official study list.
- The registered formula for LEI and PVA was described at a high level, not as equations. LEI is implemented as frequency weighted by benchmark-derived model PVR and scaled by reported minutes/duration. PVA is implemented as the mean of forced-choice avoidance, translation avoidance, and PV acceptability avoidance.
- Layer 3 human verification is represented as `final_confirmed=True` by default because a human annotation UI was not specified in the visible prompt.
- Real provider SDK calls are isolated behind `LLMClient`; without keys, deterministic mock output is returned and explicitly labelled.

## NLP Design

The prompt asks for transformer dependency parsing with `spacy` and `en_core_web_trf`. The package dependency is included, but the transformer model is not required at startup because the system must boot without extra setup. The current detector uses a deterministic PHaVE-list pattern layer with confidence metadata. A production research deployment should replace or extend `PVDetector.detect()` with dependency parses from `en_core_web_trf`.

## Persistence

SQLite foreign keys are enabled with `PRAGMA foreign_keys=ON`. ORM relationships use `ondelete="CASCADE"` plus SQLAlchemy cascades for child rows.

## Documentation Sources

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy 2.0 ORM: https://docs.sqlalchemy.org/en/20/orm/
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- spaCy pipelines/models: https://spacy.io/models/en
- PHaVE-list reference trail: Martinez 2011 / Gardner and Davies 2007 phrasal verb lists, to be replaced with the study-approved list if available.
