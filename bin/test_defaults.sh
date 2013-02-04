#!/usr/bin/env bash
export ALLOW_START="true"
if [ -z "$RUNNING" ]; then export ALLOW_START="false"; fi
if [ -z "$IMPORT" ]; then export ALLOW_START="false"; fi
if [ -z "$NZB_THREADS" ]; then export ALLOW_START="false"; fi
if [ -z "$NZBCOUNT" ]; then export ALLOW_START="false"; fi
if [ -z "$IMPORT_SLEEP" ]; then export ALLOW_START="false"; fi
if [ -z "$IMPORT_MAX_RELEASES" ]; then export ALLOW_START="false"; fi
if [ -z "$RELEASES" ]; then export ALLOW_START="false"; fi
if [ -z "$RELEASES_SLEEP" ]; then export ALLOW_START="false"; fi
if [ -z "$OPTIMIZE" ]; then export ALLOW_START="false"; fi
if [ -z "$MYISAM_SMALL" ]; then export ALLOW_START="false"; fi
if [ -z "$MYISAM_LARGE" ]; then export ALLOW_START="false"; fi
if [ -z "$INNODB_SMALL" ]; then export ALLOW_START="false"; fi
if [ -z "$INNODB_LARGE" ]; then export ALLOW_START="false"; fi
if [ -z "$INNODB" ]; then export ALLOW_START="false"; fi
if [ -z "$CLEANUP" ]; then export ALLOW_START="false"; fi
if [ -z "$CLEANUP_TIMER" ]; then export ALLOW_START="false"; fi
if [ -z "$PARSING" ]; then export ALLOW_START="false"; fi
if [ -z "$PARSING_TIMER" ]; then export ALLOW_START="false"; fi
if [ -z "$PREDB_TIMER" ]; then export ALLOW_START="false"; fi
if [ -z "$TVRAGE_TIMER" ]; then export ALLOW_START="false"; fi
if [ -z "$SPHINX" ]; then export ALLOW_START="false"; fi
if [ -z "$SPHINX_TIMER" ]; then export ALLOW_START="false"; fi
if [ -z "$SED" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_HTOP" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_NMON" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_BWMNG" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_IOTOP" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_MYTOP" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_VNSTAT" ]; then export ALLOW_START="false"; fi
if [ -z "$USE_IFTOP" ]; then export ALLOW_START="false"; fi
if [ -z "$POWERLINE" ]; then export ALLOW_START="false"; fi
if [ -z "$RAMDISK" ]; then export ALLOW_START="false"; fi
if [ -z "$AGREED" ]; then export ALLOW_START="false"; fi
if [ -z "$MYSQL" ]; then export ALLOW_START="false"; fi
if [ -z "$PHP" ]; then export ALLOW_START="false"; fi
if [ -z "$TMUXCMD" ]; then export ALLOW_START="false"; fi
if [ -z "$NICE" ]; then export ALLOW_START="false"; fi
if [ -z "$TMUX_CONF" ]; then export ALLOW_START="false"; fi
if [ -z "$RUNNING" ]; then export ALLOW_START="false"; fi
if [ -z "$NEWZPATH" ]; then export ALLOW_START="false"; fi
if [ -z "$NEWZNAB_PATH" ]; then export ALLOW_START="false"; fi
if [ -z "$TESTING_PATH" ]; then export ALLOW_START="false"; fi
if [ -z "$ADMIN_PATH" ]; then export ALLOW_START="false"; fi
if [ -z "$POST_TO_RUN" ]; then export ALLOW_START="false"; fi
if [ -z "$TMUX_SESSION" ]; then export ALLOW_START="false"; fi
if [ -z "$MONITOR_UPDATE" ]; then export ALLOW_START="false"; fi
if [ -z "$BINARIES" ]; then export ALLOW_START="false"; fi
if [ -z "$BINARIES_THREADS" ]; then export ALLOW_START="false"; fi
if [ -z "$BINARIES_SLEEP" ]; then export ALLOW_START="false"; fi
if [ -z "$MAX_RELEASES" ]; then export ALLOW_START="false"; fi
if [ -z "$BACKFILL" ]; then export ALLOW_START="false"; fi
if [ -z "$BACKFILL_THREADS" ]; then export ALLOW_START="false"; fi
if [ -z "$BACKFILL_SLEEP" ]; then export ALLOW_START="false"; fi
if [ -z "$BACKFILL_MAX_RELEASES" ]; then export ALLOW_START="false"; fi
if [ -z "$MAXDAYS" ]; then export ALLOW_START="false"; fi
if [ -z "$NZBS" ]; then export ALLOW_START="false"; fi
if [ -z "$IMPORT_MAX_ROWS" ]; then export ALLOW_START="false"; fi
if [ -z "$BINARIES_MAX_ROWS" ]; then export ALLOW_START="false"; fi
if [ -z "$BACKFILL_MAX_ROWS" ]; then export ALLOW_START="false"; fi

