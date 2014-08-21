#!/usr/bin/env python
#
# Copyright (c) 2014 Paul Osborne. All rights reserved.
# This code is released as open sourrce under the terms of the
# MIT License v2.0 (http://opensource.org/licenses/MIT)
#
import argparse
import os
import sys


def get_symlink_directory():
    """Get the directory where symlinks for aliases are stored"""
    return os.path.join(os.getenv("HOME"), ".dnav", "symlinks")


def get_target_for_alias(alias):
    """Get the full path to the directory pointed to by the provided alias

    If the alias does not exist, this method will return None

    """
    alias_path = os.path.join(get_symlink_directory(), alias)
    if not os.path.exists(alias_path):
        return None
    return os.path.abspath(os.readlink(alias_path))


def do_cd(args):
    """Cd command handler"""
    alias = args.alias

    target_directory = get_target_for_alias(alias)
    if target_directory is None:
        print("Alias %r is not defined" % (alias, ))
    sys.stdout.write(target_directory)
    return 1  # 1 is interpreted specially by the shell script wrapper


def do_add(args):
    """add command handler"""
    alias = args.alias
    alias_path = os.path.join(get_symlink_directory(), alias)
    directory = os.path.abspath(args.directory)

    if not os.path.exists(directory):
        print("Directory %r does not exist" % (directory, ))
        return -1

    if not os.path.isdir(directory):
        print("%r exists but is not a directory" % (directory, ))
        return -1

    # If this alias already exists remove it first
    if os.path.exists(alias_path):
        os.unlink(alias_path)
    os.symlink(directory, alias_path)
    print("New alias created %s -> %s" % (alias, directory))
    return 0


def do_show(args):
    """Show command handler"""
    alias = args.alias

    target_directory = get_target_for_alias(alias)
    if target_directory is None:
        print("No alias with name %r exists" % (alias, ))
        return -1

    print(target_directory)
    return 0


def do_rm(args):
    """Rm command handler"""
    alias = args.alias
    alias_path = os.path.join(get_symlink_directory(), alias)

    if not os.path.exists(alias_path):
        print("No alias with name %r exists" % (alias, ))
        return -1
    else:
        target_directory = os.path.abspath(os.readlink(alias_path))
        os.unlink(alias_path)
        print("Alias deleted: %s -> %s" % (alias, target_directory))
        return 0


def do_clear(args):
    """Clear command handler"""


def do_list(args):
    """List command handler"""


def do_prune(args):
    """Prune command handler"""


def build_argument_parser():
    """Build the argument parser for the command-line interface"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands',
        dest='subcommand',
        help='allowed commands')

    #
    # dnav cd <alias>
    #
    cd = subparsers.add_parser('cd', help='Change to directory with some alias')
    cd.add_argument('alias', help="The alias of the directory to which the shell should navigate")
    cd.set_defaults(subcommand_handler=do_cd)

    #
    # dnav add <alias> [<directory>]
    #
    add = subparsers.add_parser('add', help='Record a new directory alias')
    add.add_argument('alias', help="The new alias to be created or overwritten")
    add.add_argument('directory',
                     nargs='?',
                     default=os.getcwd(),
                     help="The directory to alias (defaults to current working directory)")
    add.set_defaults(subcommand_handler=do_add)

    #
    # dnav show <alias>
    #
    show = subparsers.add_parser('show', help='Show the directory pointed to by an alias')
    show.add_argument('alias', help='The alias to show')
    show.set_defaults(subcommand_handler=do_show)

    #
    # dnav rm <alias>
    #
    rm = subparsers.add_parser('rm', help='Remove specified alias')
    rm.add_argument('alias', help='The alias to remove')
    rm.set_defaults(subcommand_handler=do_rm)

    #
    # dnav clear
    #
    clear = subparsers.add_parser('clear', help='Clear all recorded aliases')
    clear.set_defaults(subcommand_handler=do_clear)

    #
    # dnav list
    #
    list_parser = subparsers.add_parser('list', help='List all directory aliases')
    list_parser.set_defaults(subcommand_handler=do_list)

    #
    # dnav prune
    #
    prune = subparsers.add_parser('prune', help='Remove aliases pointing to directories that no longer exist')
    prune.set_defaults(subcommand_handler=do_prune)

    return parser


def main(*args):
    parser = build_argument_parser()
    arguments = parser.parse_args(args)

    # Ensure that the symlink directory exists before getting into trouble
    if not os.path.exists(get_symlink_directory()):
        os.makedirs(get_symlink_directory())

    # Each subcommand defines a handler function.  We just need to call that
    return arguments.subcommand_handler(arguments)


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
