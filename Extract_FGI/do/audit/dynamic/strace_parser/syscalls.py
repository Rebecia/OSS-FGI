from audit.dynamic.strace_parser.syscall_parsers import *

syscall_table = {
	#
    # File operations
	#
	"CLOSE"		: { "parser" : parse_close,	"category"	: "files" },
	"CREAT"		: { "parser" : parse_create,	"category"	: "files" },
	"OPEN"		: { "parser" : parse_open,		"category"	: "files" },
	"OPENAT"	: { "parser" : parse_open,		"category"	: "files" },		
	"MKNOD"		: { "parser" : parse_default,	"category"	: "files" },
	"MKNODAT"	: { "parser" : parse_default,	"category"	: "files" },
	"RENAME"	: { "parser" : parse_rename,	"category"	: "files" },
	"RENAMEAT"	: { "parser" : parse_rename,	"category"	: "files" },
	"TRUNCATE"	: { "parser" : parse_default,	"category"	: "files" },
	"FTRUNCATE"	: { "parser" : parse_default,	"category"	: "files" },

	#
    # Directory operations
	#
	"MKDIR"		: { "parser" : parse_dir,	"category"	: "files" },
	"MKDIRAT"	: { "parser" : parse_default,	"category"	: "files" },
	"RMDIR"		: { "parser" : parse_dir,	"category"	: "files" },
	"CHDIR"	: { "parser" : parse_chdir,	"category"	: "files" },
	"CHROOT"	: { "parser" : parse_default,	"category"	: "files" },

	#
    # Link operations
	#
	"LINK"		: { "parser" : parse_link,	"category"	: "files" },
	"SYMLINK"	: { "parser" : parse_default,	"category"	: "files" },
	"SYMLINKAT"	: { "parser" : parse_default,	"category"	: "files" },
	"UNLINK"	: { "parser" : parse_dir,	"category"	: "files" },
	"UNLINKAT"	: { "parser" : parse_unlinkat,	"category"	: "files" },

	#
    # Basic file attributes
	#

	"CHMOD"		: { "parser" : parse_chmod,		"category"	: "files" },
	"FCHMOD"	: { "parser" : parse_chmod,		"category"	: "files" },
	"FCHMODAT"	: { "parser" : parse_chmod,		"category"	: "files" },
	"CHOWN"		: { "parser" : parse_default,	"category"	: "files" },
	"LCHOWN"	: { "parser" : parse_default,	"category"	: "files" },
	"FCHOWN"	: { "parser" : parse_default,	"category"	: "files" },
	"FCHOWNAT"	: { "parser" : parse_default,	"category"	: "files" },


	#
    # Extended file attributes
	#
	"SETXATTR"		: { "parser" : parse_default,	"category"	: "files" },
	"LSETXATTR"		: { "parser" : parse_default,	"category"	: "files" },
	"FSETXATTR"		: { "parser" : parse_default,	"category"	: "files" },
	"REMOVEXATTR"		: { "parser" : parse_default,	"category"	: "files" },
	"LREMOVEXATTR"		: { "parser" : parse_default,	"category"	: "files" },
	"FREMOVEXATTR"		: { "parser" : parse_default,	"category"	: "files" },

	#
    # File descriptor manipulations
	#
	"FCNTL"		: { "parser" : parse_void,	"category"	: "files" },
	"DUP"		: { "parser" : parse_void,	"category"	: "files" },
	"DUP2"		: { "parser" : parse_void,	"category"	: "files" },

	#
    # Manually added

	"TRUNCATE64"	: { "parser" : parse_default,	"category"	: "files" },
	"SENDFILE64"	: { "parser" : parse_default,	"category"	: "files" },
	"RENAMEAT2"		: { "parser" : parse_default,	"category"	: "files" },
	"FTRUNCATE64"	: { "parser" : parse_default,	"category"	: "files" },
	"LCHOWN32"		: { "parser" : parse_default,	"category"	: "files" },
	"CHOWN32"		: { "parser" : parse_default,	"category"	: "files" },
	"FCHOWN32"		: { "parser" : parse_default,	"category"	: "files" },

	"SOCKET"		: { "parser" : parse_void,		"category"	: "network" },
	"BIND"			: { "parser" : parse_bind,		"category"	: "network" },
	"LISTEN"		: { "parser" : parse_default,	"category"	: "network" },

	"CONNECT"	: { "parser" : parse_connect,	"category"	: "network" },
	"LISTEN"	: { "parser" : parse_default,	"category"	: "network" },
	"SHUTDOWN"	: { "parser" : parse_default,	"category"	: "network" },

	#
    # Send/Receive
	#
	"RECVFROM"	: { "parser" : parse_data_transfer,	"category"	: "network" },
	"SENDTO"	: { "parser" : parse_data_transfer,	"category"	: "network" },

    # Naming
	#
	"SETHOSTNAME"	: { "parser" : parse_default,	"category"	: "network" },
	"SETDOMAINNAME"	: { "parser" : parse_default,	"category"	: "network" },

	#
    # Manually added

	"RECV"	: { "parser" : parse_default,	"category"	: "network" },
	"SEND"	: { "parser" : parse_default,	"category"	: "network" },

	#
    # Process creation and termination

	"EXECVE"	: { "parser" : parse_execve,	"category"	: "process" },
	"EXECVEAT"	: { "parser" : parse_execve,	"category"	: "process" },

	#
    # Users and groups
	#
	"SETUID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETGID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETRESUID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETRESGID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETREUID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETREGID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETFSUID"	: { "parser" : parse_default,	"category"	: "process" },
	"SETFSGID"	: { "parser" : parse_default,	"category"	: "process" },

	#
    # Resource limits
	#
	"SETRLIMIT"	: { "parser" : parse_default,	"category"	: "process" },
	"PRLIMIT"	: { "parser" : parse_default,	"category"	: "process" },

}


PROCESS_SYSCALLS = {
    # Process scheduling
    "SCHED_SETATTR",
	"SCHED_GETATTR",
	"SCHED_SETSCHEDULER",
	"SCHED_GETSCHEDULER",
	"SCHED_SETPARAM",
	"SCHED_GETPARAM",
	"SCHED_SETAFFINITY",
	"SCHED_GETAFFINITY",
	"SCHED_GET_PRIORITY_MAX",
	"SCHED_GET_PRIORITY_MIN",
	"SCHED_RR_GET_INTERVAL",
	"SCHED_YIELD",
	"SETPRIORITY",
	"GETPRIORITY",
	"IOPRIO_SET",
	"IOPRIO_GET",

    # Virtual memory
    "BRK",
	"MMAP",
	"MUNMAP",
	"MREMAP",
	"MPROTECT",
	"MADVISE",
	"MLOCK",
	"MLOCK2",
	"MLOCKALL",
	"MUNLOCK",
	"MUNLOCKALL",
	"MINCORE",
	"MEMBARRIER",
	"MODIFY_LDT",

    # Threads
    "CAPSET",
	"CAPGET",
	"SET_THREAD_AREA",
	"GET_THREAD_AREA",
	"SET_TID_ADDRESS",
	"ARCH_PRCTL",

    # Miscellaneous
    "USELIB",
	"PRCTL",
	"SECCOMP",
	"PTRACE",
	"PROCESS_VM_READV",
	"PROCESS_VM_WRITEV",
	"KCMP",
	"UNSHARE",

    # Manually added
    "GETUID32",
	"SETUID32",
	"GETEGID32",
	"SETRESUID32",
	"PRLIMIT64",
	"SETREUID32",
	"MMAP2",
	"GETEUID32",
	"SETFSGID32",
    "GETGROUPS32",
	"SETGROUPS32",
	"GETRESUID32",
	"GETRESGID32",
	"GETGID32",
	"SETGID32",
	"SETRESGID32",
	"SETFSUID32",
    "SETREGID32",
	"NICE",
}

TIME_SYSCALLS = {
	#
    # Current time of day
	#
    "TIME",
	"SETTIMEOFDAY",
	"GETTIMEOFDAY",

	#
    # POSIX clocks
	#
    "CLOCK_SETTIME",
	"CLOCK_GETTIME",
	"CLOCK_GETRES",
	"CLOCK_ADJTIME",
	"CLOCK_NANOSLEEP",

	#
    # Clocks-based timers
	#
    "TIMER_CREATE",
	"TIMER_DELETE",
	"TIMER_SETTIME",
	"TIMER_GETTIME",
	"TIMER_GETOVERRUN",

	#
    # Timers
	#
    "ALARM",
	"SETITIMER",
	"GETITIMER",

	#
    # File descriptor based timers
	#
    "TIMERFD_CREATE",
	"TIMERFD_SETTIME",
	"TIMERFD_GETTIME",

	#
    # Miscellaneous
	#
    "ADJTIMEX",
	"NANOSLEEP",
	"TIMES"
}

SIGNAL_SYSCALLS = {
	#
    # Standard signals
	#
    "KILL",
	"TKILL",
	"TGKILL",
	"PAUSE",

	#
    # Real-time signals
	#
    "RT_SIGACTION",
	"RT_SIGPROCMASK",
	"RT_SIGPENDING",
	"RT_SIGQUEUEINFO",
	"RT_TGSIGQUEUEINFO",
	"RT_SIGTIMEDWAIT",
	"RT_SIGSUSPEND",
	"RT_SIGRETURN",
	"SIGALTSTACK",

	#
    # File descriptor based signals
	#
    "SIGNALFD",
	"SIGNALFD4",
	"EVENTFD",
	"EVENTFD2",

	#
    # Miscellaneous
	#
    "RESTART_SYSCALL",
	"SIGACTION",'SIGNAL','SIGPENDING','SIGPROCMASK','SIGRETURN','SIGSUSPEND'
}

IPC_SYSCALLS = {
    # IPC
    "IPC",
    # Pipe
    "PIPE",
	"PIPE2",
	"TEE",
	"SPLICE",
	"VMSPLICE",
    # Shared memory
    "SHMGET",
	"SHMCTL",
	"SHMAT",
	"SHMDT",
    # Semaphores
    "SEMGET",
	"SEMCTL",
	"SEMOP",
	"SEMTIMEDOP",
    # Futexes
    "FUTEX",
	"SET_ROBUST_LIST",
	"GET_ROBUST_LIST",
    # System V message queue
    "MSGGET",
	"MSGCTL",
	"MSGSND",
	"MSGRCV",
    # POSIX message queue
    "MQ_OPEN",
	"MQ_UNLINK",
	"MQ_GETSETATTR",
	"MQ_TIMEDSEND",
	"MQ_TIMEDRECEIVE",
	"MQ_NOTIFY"
}

KEY_MANAGEMENT_SYSCALLS = {
    # Linux key management system calls
    "ADD_KEY",
	"REQUEST_KEY",
	"KEYCTL"
}
