# Changelog

## [Unreleased]

## [1.1.0] - 2025-07-04
### Fixed
- Fixed variable value reading to properly use the `value` attribute from `<var>` elements instead of text content
- Variables defined with `<var name="NAME" value="VALUE"/>` syntax now work correctly

### Added
- Added support for shell command substitution in variable values (e.g., `$(pwd)`, `$(date)`)
- Added backward compatibility fallback for variables defined with text content
- Added explanatory comments to variable processing code

## [1.0.0] - 2025-07-03
### Added
- Initial version of `workon.py` (ported to Python 3 from legacy Python 2 script).
- Supports XML-based configuration via `~/.workon`.
- Expands `~` and `$HOME` in `<chdir>` paths.
---
