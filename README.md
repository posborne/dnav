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

Install dnav by cloning the git repo to your home directory as follows

    $ git clone https://github.com/posborne/dnav ~/.dnav

Enable shell integration (which allows dnav to modify your current
working directory) by adding the following to your `.bashrc`,
`.zshrc`, or other shell configuration file.

    source ~/.dnav/dnav.sh

That's it.  Don't forget to restart your shell or re-source your shell
init for the update to take effect.  To test, you should be able to
run the following:

    dnav --help

Basic Usage/Examples
--------------------

There aren't too many subcommands for `dnav` and they are all pretty
intuitive.  Here's the basic ones that you are likely to use most
frequently.

### Add and Navigate

    $ cd ~/Projects/wizzbang
    $ dnav add wb  # nice and short
    $ cd ../other-project
    $ dnav add op
    $ dnav cd wb
    $ pwd
    /home/user/Projects/wizzbang
    $ dnav cd op
    $ pwd
    /home/user/Projects/other-project

### List Aliases

    $ dnav list
    op -> /home/user/Projects/other-project
    wb -> /home/user/Projects/wizzbang

### Removing an Alias

    $ dnav rm op
    $ dnav list
    wb -> /home/user/Projects/wizzbang

### Cleaning up Bad Links

    $ mv ~/Projects/other-project ~/Projects/super-wizzbang
    $ dnav list
    op -> /home/user/Projects/other-project (broken)
    wb -> /home/user/Projects/wizzbang
    $ dnav prune
    Removing bad alias op -> /home/user/Projects/other-project
    $ dnav list
    wb -> /home/user/Projects/wizzbang

### Starting Fresh

    $ dnav clear

### Using dnav with other Unix Tools

    # 'dnav show <alias>' just outputs the path 'op' points to
    $ find `dnav show op` -name '*.txt'
    ...


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
