#!/bin/sh

fd . 'nautilus/' | entr -r sopel -c config.cfg
