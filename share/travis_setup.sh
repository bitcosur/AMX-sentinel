#!/bin/bash
set -evx

mkdir ~/.amerocore

# safety check
if [ ! -f ~/.amerocore/.amero.conf ]; then
  cp share/amero.conf.example ~/.amerocore/amero.conf
fi
