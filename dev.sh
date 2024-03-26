#!/bin/sh

fd . 'nautilus/' | ENV=development entr -r sopel -c config.cfg
