# `callback`

Cloudflare Tunnels.

Interact with Cloudflare WARP Tunnels.

**Usage**:

```console
$ callback [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create`: Create tunnels
* `delete`: Delete tunnels
* `list`: List existing Zero Trust tunnels
* `view`: View tunnel details

## `callback create`

Create tunnels

**Usage**:

```console
$ callback create [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cfd`: Create WARP connector
* `warp`: Create WARP connector

### `callback create cfd`

Create WARP connector

**Usage**:

```console
$ callback create cfd [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `callback create warp`

Create WARP connector

**Usage**:

```console
$ callback create warp [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `callback delete`

Delete tunnels

**Usage**:

```console
$ callback delete [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cfd`: Delete Cloudflared tunnel
* `warp`: Delete WARP tunnel

### `callback delete cfd`

Delete Cloudflared tunnel

**Usage**:

```console
$ callback delete cfd [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `callback delete warp`

Delete WARP tunnel

**Usage**:

```console
$ callback delete warp [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `callback list`

List existing Zero Trust tunnels

**Usage**:

```console
$ callback list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `callback view`

View tunnel details

**Usage**:

```console
$ callback view [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cfd`: View Cloudflared tunnel details
* `warp`: View WARP tunnel details

### `callback view cfd`

View Cloudflared tunnel details

**Usage**:

```console
$ callback view cfd [OPTIONS]
```

**Options**:

* `--name TEXT`: Tunnel name
* `--token / --no-token`: Display tunnel token  [default: no-token]
* `--help`: Show this message and exit.

### `callback view warp`

View WARP tunnel details

**Usage**:

```console
$ callback view warp [OPTIONS]
```

**Options**:

* `--name TEXT`: Tunnel name
* `--token / --no-token`: Display tunnel token  [default: no-token]
* `--help`: Show this message and exit.

