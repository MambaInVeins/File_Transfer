0809

https://unix.stackexchange.com/questions/530524/disable-stack-smashing-detected-unknown-terminated

https://sourceware.org/git/?p=glibc.git;a=blob;f=debug/stack_chk_fail.c;h=9ab9bc7cebf7ed21a13af29c860ae683ea0d29e6;hb=ed421fca42fd9b4cab7c66e77894b8dd7ca57ed0

https://sourceware.org/git/?p=glibc.git;a=blob;f=debug/fortify_fail.c;h=16549d6dbcf5b6e1f808336894c1f4778b88c5bc;hb=1ff1373b3302e9e095dc4fd4d371451c00190780


I'm not running ubuntu, but I don't think that's possible in newer versions of glibc. See this commit.

Short of writing your own stack smashing detector, of course.

You can have a look at the source of the function printing that message:

    void
    __attribute__ ((noreturn))
    __fortify_fail_abort (_Bool need_backtrace, const char *msg)
    {
    /* The loop is added only to keep gcc happy.  Don't pass down
        __libc_argv[0] if we aren't doing backtrace since __libc_argv[0]
        may point to the corrupted stack.  */
    while (1)
        __libc_message (need_backtrace ? (do_abort | do_backtrace) : do_abort,
                "*** %s ***: %s terminated\n",
                msg,
                (need_backtrace && __libc_argv[0] != NULL
                ? __libc_argv[0] : "<unknown>"));
    }
    
This function will be called with need_backtrace = False from the __stack_chk_fail, itself called from the stack protector code compiled into the binary.