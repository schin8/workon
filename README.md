# workon

The `workon` utility is a lightweight tool that launches a new subshell with the appropriate working directory and environment, based on user-defined states.

If you work on multiple projects, each with its own directory and environment variables (such as API keys, paths, or configuration settings), workon allows you to switch between them with a single command. No more manually cd-ing into directories or exporting environment variables every time you change context.

## Features

- Launch a shell in a specific directory and environment, as defined in your `~/.workon` XML configuration.
- Supports global and per-state environment variables.

## Installation

1. Copy `workon.py` to a directory in your `PATH`.
2. Make it executable:
   ```sh
   chmod +x workon.py
   [optional]
   ln -s workon.py workon
   ```

## Usage

```sh
workon.py [-h] [-l] [-n] [-v] <state>
```

- `-h`, `--help`: Show usage information.
- `-l`, `--list`: List available work states.
- `-n`, `--nochdir`, `--no-chdir`: Do not change directory.
- `-v`, `--version`: Show version information.

Example:

```sh
workon.py devops
```

## Configuration

Create a `~/.workon` file in XML format. Example:

```xml
<workon>
  <!-- Global variables: available in all states -->
  <var name="CONFIGURATION_TIMEOUT">600000</var>

  <state name="current">
    <chdir>~/src/usefulproject</chdir>
  </state>

  <state name="devops">
    <chdir>$HOME/src/cloud/CyberdineTooling</chdir>
    <var name="AWS_ACCESS_KEY_ID" value="xxxxxxxxxxxxxxx" />
    <!-- 1Password expansion of vault/item/field.  Use &quot; in place of quote --> 
    <var name="AWS_SECRET_ACCESS_KEY" value="$(op read &quot;op://devops/creds/credential&quot;)"/>
    <var name="AWS_DEFAULT_REGION" value="us-east-1" />
    <var name="AWS_PROFILE" value="dev-profile" />
  </state>

  <state name="project">
    <chdir>$HOME/src/myproject</chdir>
    <!-- Command substitution examples -->
    <var name="PROJECT_ROOT" value="$(pwd)" />
    <var name="BUILD_DATE" value="$(date +%Y%m%d)" />
    <var name="USER_NAME" value="I am $(whoami)" />
  </state>

</workon>
```

- Each `<state>` defines a work environment.
- `<chdir>` sets the working directory for that state.
- `<var>` sets environment variables with two supported syntaxes:
  - `<var name="NAME" value="VALUE" />` - Recommended attribute syntax
  - `<var name="NAME">VALUE</var>` - Text content syntax (legacy support)
  - Variables defined directly under `<workon>` are **global** and available in all states.
  - Variables inside a `<state>` are only available in that state.
- **Command substitution**: Variable values can include shell commands using `$(command)` syntax:
  - `$(pwd)` - Current working directory
  - `$(date)` - Current date/time
  - `$(whoami)` - Current username
  - Any other shell command that produces output
  
  The example var AWS_SECRET_ACCESS_KEY uses the 1Password CLI to extract an api credential.
  
  

## License

This program is free software, distributed under the GNU General Public License (GPL) v2 or later.

---

## Fork Notice

This project is a fork of the original `workon.py` utility.

**Changes and updates in this fork:**

- See changelog.md for detailed version history

**Key improvements:**
- Ported to Python 3 from the original Python 2 script
- Expands `~` and `$HOME` in `<chdir>` paths
- Fixed variable handling to properly read from `value` attributes
- Added shell command substitution support in variable values
- Backward compatibility with legacy text content variable syntax

**Original authors:**

- Ivan Nestlerode (2004)

This fork is maintained by Steven Chin , 2025.

See the original project for historical context and prior versions.

---

Originally written by Ivan Nestlerode, 2004.
Inspired by Rajesh Vaidheeswarran
