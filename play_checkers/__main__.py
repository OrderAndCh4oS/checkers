#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from play_checkers.play import play


def main():
    try:
        play()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
