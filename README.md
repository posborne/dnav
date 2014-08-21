dnav: Directory Navigator
=========================

The Problem
-----------

When working on various projects on a linux system, there are several
directories that one is likely to going to be jumping between at any
given time.  Changing between these directories can be a pain and
existing tools like `pushd` and `popd` provide support for going back
to directories that were previously pushed onto a stack.

Wouldn't it be nice if there were a command-line tool that would...

1. Allow me to jump to a directory quickly based on an alias I define?
2. Remember these aliases across shell sessions?
3. Provide familiar commands for managing directory aliases?

You're in luck.  This is what dnav is designed to provide.  Instead of
managing your directories on a stack, now you have a hash table and
you can get, put, go, rm, and clear aliases in this table with simple
commands.

Install It
----------

There are two steps to install dnav in your system and make it
usable.  These steps are the following:

1. Install dnav by cloning the git repo to your home directory as follows

    $ git clone https://github.com/posborne/dnav ~/.dnav

2. Enable shell integration (which allows dnav to modify your current
    working directory) by adding the following to your `.bashrc`,
    `.zshrc`, or other shell configuration file.

    source ~/.dnav/dnav-shell.sh

That's it.  Don't forget to restart your shell or re-source your shell
init for the update to take effect.  To test, you should be able to
run the following:

    dnav help

How Does It Work
----------------

`dnav` has two main pieces:

1. A shell script which is sourced in your shell environment that
   provides the `dnav` command.  This is necessary for `dnav` to
   change your current working directory.
2. A python scipt that implements the core functionality of `dnav`
   which is called out to by the shell function.

The only state used by `dnav` is a set of symlinks that are stored in
`~/.dnav/symlinks`.  The various `dnav` commands are just operations
on the symlinks in this directory.  For instance, the command `dnav
prune` just goes through this directory and removes any links which
point to targets that are no longer present.
