# General Information

> Source: https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html

<<<
Previous
Home
Next
>>>

The Open Group Base Specifications Issue 8

IEEE Std 1003.1-2024

Copyright © 2001-2024 The IEEE and The Open Group

2. General Information

This chapter covers information that is relevant to all the functions specified in 3. System Interfaces and XBD 14.
Headers.

2.1 Use and Implementation of Interfaces

2.1.1 Use and Implementation of Functions

Each of the following statements shall apply to all functions unless explicitly stated otherwise in the detailed descriptions
that follow:

If an argument to a function has an invalid value, such as a value outside the domain of the function, a pointer to an object
whose lifetime has ended (even if a new object now has the same address), a pointer outside the address space of the program, or a
null pointer, the behavior is undefined.

Any function declared in a header may also be implemented as a macro defined in the header, so a function should not be declared
explicitly if its header is included. Any macro definition of a function can be suppressed locally by enclosing the name of the
function in parentheses, because the name is then not followed by the <left-parenthesis> that indicates expansion of a macro
function name. For the same syntactic reason, it is permitted to take the address of a function even if it is also defined as a
macro. The use of the C-language #undef construct to remove any such macro definition shall also ensure that an actual
function is referred to.

Any invocation of a function that is implemented as a macro shall expand to code that evaluates each of its arguments exactly
once, fully protected by parentheses where necessary, so it is generally safe to use arbitrary expressions as arguments.

For functions from the ISO C standard only, provided that the function can be declared without reference to any type
defined in a header from the ISO C standard, it is also permissible to declare the function explicitly and use it without
including its associated header.

If a function that accepts a variable number of arguments is not declared (explicitly or by including its associated header),
the behavior is undefined.

Functions shall prevent data races as follows: A function shall not directly or indirectly access objects accessible by threads
other than the current thread unless the objects are accessed directly or indirectly via the function's arguments. A function shall
not directly or indirectly modify objects accessible by threads other than the current thread unless the objects are accessed
directly or indirectly via the function's non-const arguments. Implementations may share their own internal objects between threads
if the objects are not visible to applications and are protected against data races.

Functions shall perform all operations solely within the current thread if those operations have effects that are visible to
applications.

2.1.2 Use and Implementation of Macros

Each of the following statements shall apply to all macros unless explicitly stated otherwise:

Any definition of an object-like macro in a header shall expand to code that is fully protected by parentheses where necessary,
so that it groups in an arbitrary expression as if it were a single identifier.

All object-like macros listed as expanding to integer constant expressions shall additionally be suitable for use in #if
preprocessing directives.

Any definition of a function-like macro in a header shall expand to code that evaluates each of its arguments exactly once,
fully protected by parentheses where necessary, so that it is generally safe to use arbitrary expressions as arguments.

Any definition of a function-like macro in a header can be invoked in an expression anywhere a function with a compatible return
type could be called.

2.2 The Compilation Environment

2.2.1 POSIX.1 Symbols

Certain symbols in this volume of POSIX.1-2024 are defined in headers (see XBD 14. Headers). Some of those headers could also define symbols other than those
defined by POSIX.1-2024, potentially conflicting with symbols used by the application. Also, POSIX.1-2024 defines symbols that are
not permitted by other standards to appear in those headers without some control on the visibility of those symbols.

Symbols called "feature test macros" are used to control the visibility of symbols that might be included in a header.
Implementations, future versions of this standard, and other standards may define additional feature test macros.

In the compilation of an application that #defines a feature test macro specified by POSIX.1-2024, no header defined by
POSIX.1-2024 shall be included prior to the definition of the feature test macro. This restriction also applies to any
implementation-provided header in which these feature test macros are used. If the definition of the macro does not precede the
#include, the result is undefined.

Feature test macros shall begin with the <underscore> character ('_').

2.2.1.1 The _POSIX_C_SOURCE Feature Test Macro

A POSIX-conforming application shall ensure that the feature test macro _POSIX_C_SOURCE is defined before inclusion of any
header.

When an application includes a header described by POSIX.1-2024, and when this feature test macro is defined to have the value
202405L:

All symbols required by POSIX.1-2024 to appear when the header is included shall be made visible.

Symbols that are explicitly permitted, but not required, by POSIX.1-2024 to appear in that header (including those in reserved
name spaces) may be made visible.

Additional symbols not required or explicitly permitted by POSIX.1-2024 to be in that header shall not be made visible, except
when enabled by another feature test macro.

Identifiers in POSIX.1-2024 may only be undefined using the #undef directive as described in 2.1 Use
and Implementation of Interfaces or 2.2.2 The Name Space. These #undef directives shall
follow all #include directives of any header in POSIX.1-2024.

Note:
The POSIX.1-1990 standard specified a macro called _POSIX_SOURCE. This has been superseded by _POSIX_C_SOURCE.

2.2.1.2 The _XOPEN_SOURCE Feature Test Macro

[XSI]
An XSI-conforming application shall ensure that the feature test macro _XOPEN_SOURCE is defined with the value 800 before inclusion
of any header. This is needed to enable the functionality described in 2.2.1.1 The _POSIX_C_SOURCE
Feature Test Macro and to ensure that the XSI option is enabled.

Since this volume of POSIX.1-2024 is aligned with the ISO C standard, and since all functionality enabled by
_POSIX_C_SOURCE set equal to 202405L is enabled by _XOPEN_SOURCE set equal to 800, there should be no need to define
_POSIX_C_SOURCE if _XOPEN_SOURCE is so defined. Therefore, if _XOPEN_SOURCE is set equal to 800 and _POSIX_C_SOURCE is set equal to
202405L, the behavior is the same as if only _XOPEN_SOURCE is defined and set equal to 800. However, should _POSIX_C_SOURCE be set
to a value greater than 202405L, the behavior is unspecified.

If _XOPEN_SOURCE is defined with the value 800 and _POSIX_C_SOURCE is undefined before inclusion of any header, then the header
may define the _POSIX_C_SOURCE macro with the value 202405L.

2.2.1.3 The __STDC_WANT_LIB_EXT1__ Feature Test Macro

A POSIX-conforming [XSI]   or XSI-conforming
application can define the feature test macro __STDC_WANT_LIB_EXT1__ before inclusion of any header.

When an application includes a header described by POSIX.1-2024, and when this feature test macro is defined to have the value
1, the header may make visible those symbols specified for the header in Annex K of the ISO C standard that are not already
explicitly permitted by POSIX.1-2024 to be made visible in the header. These symbols are listed in 2.2.2
The Name Space below.

When an application includes a header described by POSIX.1-2024, and when this feature test macro is either undefined or defined
to have the value 0, the header shall not make any additional symbols visible that are not already made visible by the feature test
macro _POSIX_C_SOURCE [XSI]   or _XOPEN_SOURCE   as
described above, except when enabled by another feature test macro.

2.2.2 The Name Space

All identifiers in this volume of POSIX.1-2024, except environ, are defined in at least one of the headers, as shown in
XBD 14. Headers. When [XSI]
_XOPEN_SOURCE or  _POSIX_C_SOURCE is defined, each header
defines or declares some identifiers, potentially conflicting with identifiers used by the application. The set of identifiers
visible to the application consists of precisely those identifiers from the header pages of the included headers, as well as
additional identifiers reserved for the implementation. In addition, some headers may make visible identifiers from other headers
as indicated on the relevant header pages.

Implementations may also add members to a structure or union without controlling the visibility of those members with a feature
test macro, as long as a user-defined macro with the same name cannot interfere with the correct interpretation of the program. The
identifiers reserved for use by the implementation are described below:

Each identifier with external linkage described in the header section is reserved for use as an identifier with external linkage
if the header is included.

Each macro described in the header section is reserved for any use if the header is included.

Each identifier with file scope described in the header section is reserved for use as a macro name and as an identifier with
file scope in the same name space if the header is included.

As described in 13. Namespace and Future Directions, the prefixes
posix_, POSIX_, and _POSIX_ are reserved for use by POSIX.1-2024 and other POSIX standards. Implementations may add symbols to the
headers shown in the following table, provided the identifiers for those symbols either:

Begin with the corresponding reserved prefixes in the table, or

Have one of the corresponding complete names in the table, or

End in the string indicated as a reserved suffix in the table and do not use the reserved prefixes posix_, POSIX_, or _POSIX_,
as long as the reserved suffix is in that part of the name considered significant by the implementation.

Symbols that use the reserved prefix _POSIX_ may be made visible by implementations in any header defined by POSIX.1-2024.

Header

Prefix

Suffix

Complete Name

<aio.h>

aio_, lio_, AIO_, LIO_

<arpa/inet.h>

inet_

<ctype.h>

to[a-z], is[a-z]

<dlfcn.h>

RTLD_, dli_

<dirent.h>

d_, DT_

<fcntl.h>

l_

[XSI]  <fmtmsg.h>

MM_

<fnmatch.h>

FNM_

[XSI]  <ftw.h>

FTW

<glob.h>

gl_, GLOB_

<grp.h>

gr_

<libintl.h>

TEXTDOMAINMAX

<limits.h>

_MAX, _MIN

[XSI]  <math.h>

M_

[MSG]  <mqueue.h>

mq_, MQ_

[XSI]  <ndbm.h>

dbm_, DBM_

<netdb.h>

ai_, h_, n_, p_, s_

<net/if.h>

if_, IF_

<netinet/in.h>

in_, ip_, s_, sin_, INADDR_,

IPPROTO_

[IP6]

in6_, in6addr_, s6_, sin6_, IPV6_

<netinet/tcp.h>

TCP_

<nl_types.h>

NL_

<poll.h>

pd_, ph_, ps_, POLL

<pthread.h>

pthread_, PTHREAD_

<pwd.h>

pw_

<regex.h>

re_, rm_, REG_

<sched.h>

sched_, SCHED_

<semaphore.h>

sem_, SEM_

[CX]  <signal.h>

sa_, si_, sigev_, sival_, uc_, BUS_,

CLD_, FPE_, ILL_, SA_, SEGV_, SI_,

SIGEV_,

[XSI]

ss_, sv_, SS_, TRAP_

<stdatomic.h>

atomic_[a-z], memory_[a-z]

<stdlib.h>

str[a-z]

<string.h>

str[a-z], mem[a-z], wcs[a-z]

[XSI]  <sys/ipc.h>

ipc_, IPC_

key, pad, seq

<sys/mman.h>

shm_, MAP_, MCL_, MS_,

PROT_

[XSI]  <sys/msg.h>

msg, MSG_[A-Z]

msg

[XSI]  <sys/resource.h>

rlim_, ru_, PRIO_, RLIMIT_,

RUSAGE_

<sys/select.h>

fd_, fds_, FD_

Header

Prefix

Suffix

Complete Name

[XSI]  <sys/sem.h>

sem, SEM_

sem

[XSI]  <sys/shm.h>

shm, SHM[A-Z], SHM_[A-Z]

<sys/socket.h>

cmsg_, if_, ifc_, ifra_, ifru_,

infu_, l_, msg_, sa_, ss_,

[XSI]

AF_, MSG_, PF_, SCM_,

SHUT_, SO

<sys/stat.h>

st_

<sys/statvfs.h>

f_, ST_

[XSI]  <sys/time.h>

tv_

<sys/times.h>

tms_

[XSI]  <sys/uio.h>

iov_

UIO_MAXIOV

<sys/un.h>

sun_

<sys/utsname.h>

uts_

<sys/wait.h>

P_, W[A-Z]

[XSI]  <syslog.h>

LOG_

<termios.h>

c_, B[0-9], TC, ws_

<threads.h>

cnd_[a-z], mtx_[a-z], thrd_[a-z],

tss_[a-z]

[CX]  <time.h>

clock_, it_, timer_, tm_, tv_,

CLOCK_, TIMER_

[XSI]  <utmpx.h>

ut_

_LVL, _PROCESS,

_TIME

<wchar.h>

wcs[a-z]

<wctype.h>

is[a-z], to[a-z]

<wordexp.h>

we_, WRDE_

[CX]  ANY header

_t

Note:
The notation [0-9] indicates any digit. The notation [A-Z] indicates any uppercase letter in the portable character set. The
notation [a-z] indicates any lowercase letter in the portable character set. Commas and spaces in the lists of prefixes and
complete names in the above table are not part of any prefix or complete name. The ISO C standard reserves int[0-9a-z_]*_t and
uint[0-9a-z_]*_t in <stdint.h>; this is not included in the table above
because it is covered by the reserved _t suffix for any header.

Additional symbolic constants with the prefix _CS_, _PC_, and _SC_ may be defined by the inclusion of <unistd.h>, but as these are already reserved for the implementation, they are not
included in the table above. Extensions with these prefixes should be compatible with use by confstr(), pathconf(), and sysconf(), respectively.

Implementations may also add symbols to the <complex.h>
header with the following complete names or the same names suffixed with 'f' or 'l':

cerf

cexpm1

clog2

cerfc

clog10

clgamma

cexp2

clog1p

ctgamma

If any header in the following table is included, macros with the prefixes or suffixes shown may be defined. After
the last inclusion of a given header, an application may use identifiers with the corresponding prefixes for its own purpose,
provided their use is preceded by a #undef of the corresponding macro.

Header

Prefix

Suffix

<endian.h>

_ENDIAN

<errno.h>

E[0-9], E[A-Z]

<fcntl.h>

F_, O_

<fenv.h>

FE_[A-Z]

<inttypes.h>

PRI[Xa-z], SCN[Xa-z]

<locale.h>

LC_[A-Z]

<math.h>

FP_[A-Z]

<netinet/in.h>

IMPLINK_, IN_, IP_, IPPORT_, SOCK_,

[IP6]

IN6_

<signal.h>

SIG_, SIG[A-Z],

[XSI]

SV_

<stdatomic.h>

ATOMIC_[A-Z]

[CX]  <stdio.h>

SEEK_

[XSI]  <sys/resource.h>

RLIM_

[XSI]  <sys/socket.h>

CMSG_

<sys/stat.h>

S_

[XSI]  <sys/uio.h>

IOV_

<termios.h>

I, O, V (See below.)

<time.h>

TIME_[A-Z]

<unistd.h>

SEEK_

The following are used to reserve complete names for the <stdint.h> header:

INT[0-9A-Za-z_]*_MIN
INT[0-9A-Za-z_]*_MAX
INT[0-9A-Za-z_]*_C
UINT[0-9A-Za-z_]*_MIN
UINT[0-9A-Za-z_]*_MAX
UINT[0-9A-Za-z_]*_C

Note:
The notation [0-9] indicates any digit. The notation [A-Z] indicates any uppercase letter in the portable character set. The
notation [Xa-z] indicates the character 'X' or any lowercase letter in the portable character set. The notation
[0-9A-Za-z_]* indicates zero or more occurrences of any of the following: a digit, an uppercase or lowercase letter in the portable
character set, or an <underscore>.

[XSI]  The following reserved names are used as exact matches for <termios.h>:

CBAUD

EXTB

VDSUSP

DEFECHO

FLUSHO

VLNEXT

ECHOCTL

LOBLK

VREPRINT

ECHOKE

PENDIN

VSTATUS

ECHOPRT

SWTCH

VWERASE

EXTA

VDISCARD

When the feature test macro__STDC_WANT_LIB_EXT1__ is defined with the value 1 (see 2.2.1
POSIX.1 Symbols), implementations may add symbols to the headers shown in the following table provided the identifiers for
those symbols have one of the corresponding complete names in the table.

Header

Complete Name

<stdio.h>

fopen_s, fprintf_s, freopen_s, fscanf_s, gets_s, printf_s, scanf_s, snprintf_s, sprintf_s, sscanf_s, tmpfile_s,
tmpnam_s, vfprintf_s, vfscanf_s, vprintf_s, vscanf_s, vsnprintf_s, vsprintf_s, vsscanf_s

<stdlib.h>

abort_handler_s, bsearch_s, getenv_s, ignore_handler_s, mbstowcs_s, qsort_s, set_constraint_handler_s, wcstombs_s,
wctomb_s

<time.h>

asctime_s, ctime_s, gmtime_s, localtime_s

<wchar.h>

fwprintf_s, fwscanf_s, mbsrtowcs_s, snwprintf_s, swprintf_s, swscanf_s, vfwprintf_s, vfwscanf_s, vsnwprintf_s,
vswprintf_s, vswscanf_s, vwprintf_s, vwscanf_s, wcrtomb_s, wmemcpy_s, wmemmove_s, wprintf_s, wscanf_s

When the feature test macro__STDC_WANT_LIB_EXT1__ is defined with the value 1 (see 2.2.1
POSIX.1 Symbols), if any header in the following table is included, macros with the complete names shown may be defined.

Header

Complete Name

<stdint.h>

RSIZE_MAX

<stdio.h>

L_tmpnam_s, TMP_MAX_S

Note:
The above two tables only include those symbols from Annex K of the ISO C standard that are not already allowed to be
visible by entries in earlier tables in this section.

The following identifiers are reserved regardless of the inclusion of headers:

1.
With the exception of identifiers beginning with the prefix _POSIX_ and those identifiers which are lexically identical to
keywords defined by the ISO C standard (for example _Bool), all identifiers that begin with an <underscore> and
either an uppercase letter or another <underscore> are always reserved for any use by the implementation.
2.
All identifiers that begin with an <underscore> are always reserved for use as identifiers with file scope in both the
ordinary identifier and tag name spaces.
3.
All identifiers in the table below are reserved for use as identifiers with external linkage. Some of these identifiers do not
appear in this volume of POSIX.1-2024, but are reserved for future use by the ISO C standard.
4.
All functions and external identifiers defined in XBD 14. Headers are
reserved for use as identifiers with external linkage.
5.
All the identifiers defined in this volume of POSIX.1-2024 that have external linkage and errno are always reserved for
use as identifiers with external linkage.

Note:
The notation [a-z] indicates any lowercase letter in the portable character set. The notation '*' indicates any
combination of digits, letters in the portable character set, or <underscore>.

No other identifiers are reserved.

_Exit

abort

abs

acos

acosf

acosh

acoshf

acoshl

acosl

aligned_alloc

asctime

asin

asinf

asinh

asinhf

asinhl

asinl

at_quick_exit

atan

atan2

atan2f

atan2l

atanf

atanh

atanhf

atanhl

atanl

atexit

atof

atoi

atol

atoll

atomic_compare_exchange_strong

atomic_compare_exchange_strong_explicit

atomic_compare_exchange_weak

atomic_compare_exchange_weak_explicit

atomic_exchange

atomic_exchange_explicit

atomic_fetch_add

atomic_fetch_add_explicit

atomic_fetch_and

atomic_fetch_and_explicit

atomic_fetch_or

atomic_fetch_or_explicit

atomic_fetch_sub

atomic_fetch_sub_explicit

atomic_fetch_xor

atomic_fetch_xor_explicit

atomic_flag_clear

atomic_flag_clear_explicit

atomic_flag_test_and_set

atomic_flag_test_and_set_explicit

atomic_init

atomic_is_lock_free

atomic_load

atomic_load_explicit

atomic_signal_fence

atomic_store

atomic_store_explicit

atomic_thread_fence

bsearch

btowc

c16rtomb

c32rtomb

cabs

cabsf

cabsl

cacos

cacosf

cacosh

cacoshf

cacoshl

cacosl

call_once

calloc

carg

cargf

cargl

casin

casinf

casinh

casinhf

casinhl

casinl

catan

catanf

catanh

catanhf

catanhl

catanl

cbrt

cbrtf

cbrtl

ccos

ccosf

ccosh

ccoshf

ccoshl

ccosl

ceil

ceilf

ceill

cerf

cerfc

cerfcf

cerfcl

cerff

cerfl

cexpm1

cexpm1f

cexpm1l

cexp

cexp2

cexp2f

cexp2l

cexpf

cexpl

cimag

cimagf

cimagl

clearerr

clgamma

clgammaf

clgammal

clock

clog

clog10

clog10f

clog10l

clog1p

clog1pf

clog1pl

clog2

clog2f

clog2l

clogf

clogl

cnd_broadcast

cnd_destroy

cnd_init

cnd_signal

cnd_timedwait

cnd_wait

conj

conjf

conjl

copysign

copysignf

copysignl

cos

cosf

cosh

coshf

coshl

cosl

cpow

cpowf

cpowl

cproj

cprojf

cprojl

creal

crealf

creall

csin

csinf

csinh

csinhf

csinhl

csinl

csqrt

csqrtf

csqrtl

ctan

ctanf

ctanh

ctanhf

ctanhl

ctanl

ctgamma

ctgammaf

ctgammal

ctime

difftime

div

erf

erfc

erfcf

erfcl

erff

erfl

errno

exit

exp

exp2

exp2f

exp2l

expf

expl

expm1

expm1f

expm1l

fabs

fabsf

fabsl

fclose

fdim

fdimf

fdiml

feclearexcept

fegetenv

fegetexceptflag

fegetround

feholdexcept

feof

feraiseexcept

ferror

fesetenv

fesetexceptflag

fesetround

fetestexcept

feupdateenv

fflush

fgetc

fgetpos

fgets

fgetwc

fgetws

floor

floorf

floorl

fma

fmaf

fmal

fmax

fmaxf

fmaxl

fmin

fminf

fminl

fmod

fmodf

fmodl

fopen

fprintf

fputc

fputs

fputwc

fputws

fread

free

freopen

frexp

frexpf

frexpl

fscanf

fseek

fsetpos

ftell

fwide

fwprintf

fwrite

fwscanf

getc

getchar

getenv

getwc

getwchar

gmtime

hypot

hypotf

hypotl

ilogb

ilogbf

ilogbl

imaxabs

imaxdiv

is[a-z]*

kill_dependency

labs

ldexp

ldexpf

ldexpl

ldiv

lgamma

lgammaf

lgammal

llabs

lldiv

llrint

llrintf

llrintl

llround

llroundf

llroundl

localeconv

localtime

log

log10

log10f

log10l

log1p

log1pf

log1pl

log2

log2f

log2l

logb

logbf

logbl

logf

logl

longjmp

lrint

lrintf

lrintl

lround

lroundf

lroundl

malloc

math_errhandling

mblen

mbrlen

mbrtoc16

mbrtoc32

mbrtowc

mbsinit

mbsrtowcs

mbstowcs

mbtowc

mem[a-z]*

mktime

modf

modff

modfl

mtx_destroy

mtx_init

mtx_lock

mtx_timedlock

mtx_trylock

mtx_unlock

nan

nanf

nanl

nearbyint

nearbyintf

nearbyintl

nextafter

nextafterf

nextafterl

nexttoward

nexttowardf

nexttowardl

perror

pow

powf

powl

printf

putc

putchar

puts

putwc

putwchar

qsort

quick_exit

raise

rand

realloc

remainder

remainderf

remainderl

remove

remquo

remquof

remquol

rename

rewind

rint

rintf

rintl

round

roundf

roundl

scalbln

scalblnf

scalblnl

scalbn

scalbnf

scalbnl

scanf

setbuf

setjmp

setlocale

setvbuf

signal

sin

sinf

sinh

sinhf

sinhl

sinl

snprintf

sprintf

sqrt

sqrtf

sqrtl

srand

sscanf

str[a-z]*

swprintf

swscanf

system

tan

tanf

tanh

tanhf

tanhl

tanl

tgamma

tgammaf

tgammal

thrd_create

thrd_current

thrd_detach

thrd_equal

thrd_exit

thrd_join

thrd_sleep

thrd_yield

time

timespec_get

tmpfile

tmpnam

to[a-z]*

trunc

truncf

truncl

tss_create

tss_delete

tss_get

tss_set

ungetc

ungetwc

va_copy

va_end

vfprintf

vfscanf

vfwprintf

vfwscanf

vprintf

vscanf

vsnprintf

vsprintf

vsscanf

vswprintf

vswscanf

vwprintf

vwscanf

wcrtomb

wcs[a-z]*

wctob

wctomb

wctrans

wctype

wmemchr

wmemcmp

wmemcpy

wmemmove

wmemset

wprintf

wscanf

Note:
The notation [a-z] indicates any lowercase letter in the portable character set. The notation '*' indicates any
sequence of zero or more characters that are valid in identifiers with external linkage.

Applications shall not declare or define identifiers with the same name as an identifier reserved in the same
context. Since macro names are replaced whenever found, independent of scope and name space, macro names matching any of the
reserved identifier names shall not be defined by an application if any associated header is included.

Except that the effect of each inclusion of <assert.h> depends
on the definition of NDEBUG, headers may be included in any order, and each may be included more than once in a given scope, with
no difference in effect from that of being included only once.

If used, the application shall ensure that a header is included outside of any external declaration or definition,
and it shall be first included before the first reference to any type or macro it defines, or to any function or object it
declares. However, if an identifier is declared or defined in more than one header, the second and subsequent associated headers
may be included after the initial reference to the identifier. Prior to the inclusion of a header, or when any macro defined in the
header is expanded, the application shall not define any macros with names lexically identical to symbols defined by that
header.

2.3 Error Numbers

Most functions can provide an error number. The means by which each function provides its error numbers is
specified in its description.

Some functions provide the error number in a variable accessed through the symbol errno, defined by
including the <errno.h> header. The value of errno should only be
examined when it is indicated to be valid by a function's return value. No function in this volume of POSIX.1-2024 shall set
errno to zero. For each thread of a process, the value of errno shall not be affected by function calls or
assignments to errno by other threads.

Some functions return an error number directly as the function value. These functions return a value of zero to
indicate success.

If more than one error occurs in processing a function call, any one of the possible errors may be returned, as the
order of detection is undefined.

Implementations may support additional errors not included in this list, may generate errors included in this list
under circumstances other than those described here, or may contain extensions or limitations that prevent some errors from
occurring.

The ERRORS section on each reference page specifies which error conditions shall be detected by all implementations
("shall fail") and which may be optionally detected by an implementation ("may fail"). If no error condition is detected, the
action requested shall be successful. If an error condition is detected, the action requested may have been partially performed,
unless otherwise stated.

Implementations may generate error numbers listed here under circumstances other than those described, if and only
if all those error conditions can always be treated identically to the error conditions as described in this volume of
POSIX.1-2024. Implementations shall not generate a different error number from one required by this volume of POSIX.1-2024 for an
error condition described in this volume of POSIX.1-2024, but may generate additional errors unless explicitly disallowed for a
particular function.

Each implementation shall document, in the conformance document, situations in which each of the optional
conditions defined in POSIX.1-2024 is detected. The conformance document may also contain statements that one or more of the
optional error conditions are not detected.

Certain threads-related functions are not allowed to return an error code of [EINTR]. Where this applies it is
stated in the ERRORS section on the individual function pages.

The following macro names identify the possible error numbers, in the context of the functions specifically defined
in this volume of POSIX.1-2024; these general descriptions are more precisely defined in the ERRORS sections of the functions that
return them. Only these macro names should be used in programs, since the actual value of the error number is unspecified. All
values listed in this section shall be unique, except as noted below. The values for all these macros shall be found in the
<errno.h> header defined in the Base Definitions volume of POSIX.1-2024. The
actual values are unspecified by this volume of POSIX.1-2024.

[E2BIG]

Argument list too long. The sum of the number of bytes used by the new process image's argument list and environment list is
greater than the system-imposed limit of {ARG_MAX} bytes.

or:

Lack of space in an output buffer.

or:

Argument is greater than the system-imposed maximum.

[EACCES]

Permission denied. An attempt was made to access a file in a way forbidden by its file access permissions.
[EADDRINUSE]

Address in use. The specified address is in use.
[EADDRNOTAVAIL]

Address not available. The specified address is not available from the local system.
[EAFNOSUPPORT]

Address family not supported. The implementation does not support the specified address family, or the specified address is not a
valid address for the address family of the specified socket.
[EAGAIN]

Resource temporarily unavailable. This is a temporary condition and later calls to the same routine may complete normally.
[EALREADY]

Connection already in progress. A connection request is already in progress for the specified socket.
[EBADF]

Bad file descriptor. A file descriptor argument is out of range, refers to no open file, or a read (write) request is made to a
file that is only open for writing (reading).
[EBADMSG]

Bad Message. The implementation has detected a corrupted message.
[EBUSY]

Resource busy. An attempt was made to make use of a system resource that is not currently available, as it is being used by another
process in a manner that would have conflicted with the request being made by this process.
[ECANCELED]

Operation canceled. The associated asynchronous operation was canceled before completion.
[ECHILD]

No child process. A wait(), waitid(), or
waitpid() function was executed by a process that had no existing or unwaited-for
child process.
[ECONNABORTED]

Connection aborted. The connection has been aborted.
[ECONNREFUSED]

Connection refused. An attempt to connect to a socket was refused because there was no process listening or because the queue of
connection requests was full and the underlying protocol does not support retransmissions.
[ECONNRESET]

Connection reset. The connection was forcibly closed by the peer.
[EDEADLK]

Resource deadlock would occur. An attempt was made to lock a system resource that would have resulted in a deadlock situation.
[EDESTADDRREQ]

Destination address required. No bind address was established.
[EDOM]

Domain error. An input argument is outside the defined domain of the mathematical function (defined in the ISO C
standard).
[EDQUOT]

Reserved.
[EEXIST]

File exists. An existing file was mentioned in an inappropriate context; for example, as a new link name in the link() function.
[EFAULT]

Bad address. The system detected an invalid address in attempting to use an argument of a call. The reliable detection of this
error cannot be guaranteed, and when not detected may result in the generation of a signal, indicating an address violation, which
is sent to the process.
[EFBIG]

File too large. The size of a file would exceed the implementation's maximum file size, the file size limit of the process, or the
offset maximum established in the corresponding open file description.
[EHOSTUNREACH]

Host is unreachable. The destination host cannot be reached (probably because the host is down or a remote router cannot reach
it).
[EIDRM]

Identifier removed. Returned during XSI interprocess communication if an identifier has been removed from the system.
[EILSEQ]

Illegal byte sequence. A wide-character code has been detected that does not correspond to a valid character, or a byte sequence
does not form a valid wide-character code (defined in the ISO C standard).
[EINPROGRESS]

Operation in progress. This code is used to indicate that an asynchronous operation has not yet completed.

or:

O_NONBLOCK is set for the socket file descriptor and the connection cannot be immediately established.

[EINTR]

Interrupted function call. An asynchronous signal was caught by the process during the execution of an interruptible function. If
the signal handler performs a normal return, the interrupted function call may return this condition (see the Base Definitions
volume of POSIX.1-2024, <signal.h>).
[EINVAL]

Invalid argument. Some invalid argument was supplied; for example, specifying an undefined signal in a signal() function or a kill() function.
[EIO]

Input/output error. Some physical input or output error has occurred. This error may be reported on a subsequent operation on the
same file descriptor. Any other error-causing operation on the same file descriptor may cause the [EIO] error indication to be
lost.
[EISCONN]

Socket is connected. The specified socket is already connected.
[EISDIR]

Is a directory. An attempt was made to open a directory with write mode specified.
[ELOOP]

Symbolic link loop. A loop exists in symbolic links encountered during pathname resolution. This error may also be returned if more
than {SYMLOOP_MAX} symbolic links are encountered during pathname resolution.
[EMFILE]

File descriptor value too large or too many open streams. An attempt was made to open a file descriptor with a value greater than
or equal to {OPEN_MAX}, [XSI]   or greater than or equal to the soft limit RLIMIT_NOFILE for the process (if smaller than
{OPEN_MAX});   or an attempt was made to open more than the
maximum number of streams allowed in the process.
[EMLINK]

Too many hard links. An attempt was made to have the link count of a single file exceed {LINK_MAX}.
[EMSGSIZE]

Message too large. A message sent on a transport provider was larger than an internal message buffer or some other network limit.

or:

Inappropriate message buffer length.

[EMULTIHOP]

Reserved.
[ENAMETOOLONG]

Filename too long. The length of a pathname exceeds {PATH_MAX} and the implementation considers this to be an error, or a pathname
component is longer than {NAME_MAX}. This error may also occur when pathname substitution, as a result of encountering a symbolic
link during pathname resolution, results in a pathname string the size of which exceeds {PATH_MAX}.
[ENETDOWN]

Network is down. The local network interface used to reach the destination is down.
[ENETRESET]

The connection was aborted by the network.
[ENETUNREACH]

Network unreachable. No route to the network is present.
[ENFILE]

Too many files open in system. Too many files are currently open in the system. The system has reached its predefined limit for
simultaneously open files and temporarily cannot accept requests to open another one.
[ENOBUFS]

No buffer space available. Insufficient buffer resources were available in the system to perform the socket operation.
[ENODEV]

No such device. An attempt was made to apply an inappropriate function to a device; for example, trying to read a write-only device
such as a printer.
[ENOENT]

No such file or directory. A component of a specified pathname does not exist, or the pathname is an empty string.
[ENOEXEC]

Executable file format error. A request is made to execute a file that, although it has appropriate privileges, is not in the
format required by the implementation for executable files.
[ENOLCK]

No locks available. A system-imposed limit on the number of simultaneous file and record locks has been reached and no more are
currently available.
[ENOLINK]

Reserved.
[ENOMEM]

Not enough space. The new process image requires more memory than is allowed by the hardware or system-imposed memory management
constraints.
[ENOMSG]

No message of the desired type. The message queue does not contain a message of the required type during XSI interprocess
communication.
[ENOPROTOOPT]

Protocol not available. The protocol option specified to setsockopt() is not
supported by the implementation.
[ENOSPC]

No space left on a device. During the write() function on a regular file or when
extending a directory, there is no free space left on the device.
[ENOSYS]

Functionality not supported. An attempt was made to use optional functionality that is not supported in this implementation.
[ENOTCONN]

Socket not connected. The socket is not connected.
[ENOTDIR]

Not a directory. A component of the specified pathname exists, but it is not a directory, when a directory was expected; or an
attempt was made to create a non-directory file, and the specified pathname contains at least one non-<slash> character and
ends with one or more trailing <slash> characters.
[ENOTEMPTY]

Directory not empty. A directory other than an empty directory was supplied when an empty directory was expected.
[ENOTRECOVERABLE]

State not recoverable. The state protected by a robust mutex is not recoverable.
[ENOTSOCK]

Not a socket. The file descriptor does not refer to a socket.
[ENOTSUP]

Not supported. The implementation does not support the requested feature or value.
[ENOTTY]

Inappropriate I/O control operation. A control function has been attempted for a file or special file for which the operation is
inappropriate.
[ENXIO]

No such device or address. Input or output on a special file refers to a device that does not exist, or makes a request beyond the
capabilities of the device. It may also occur when, for example, a tape drive is not on-line.
[EOPNOTSUPP]

Operation not supported on socket. The type of socket (address family or protocol) does not support the requested operation. A
conforming implementation may assign the same values for [EOPNOTSUPP] and [ENOTSUP].
[EOVERFLOW]

Value too large to be stored in data type. An operation was attempted which would generate a value that is outside the range of
values that can be represented in the relevant data type or that are allowed for a given data item.
[EOWNERDEAD]

Previous owner died. The owner of a robust mutex terminated while holding the mutex lock.
[EPERM]

Operation not permitted. An attempt was made to perform an operation limited to processes with appropriate privileges or to the
owner of a file or other resource.
[EPIPE]

Broken pipe. A write was attempted on a socket, pipe, or FIFO for which there is no process to read the data.
[EPROTO]

Protocol error. Some protocol error occurred. This error is device-specific, but is generally not related to a hardware
failure.
[EPROTONOSUPPORT]

Protocol not supported. The protocol is not supported by the address family, or the protocol is not supported by the
implementation.
[EPROTOTYPE]

Protocol wrong type for socket. The socket type is not supported by the protocol.
[ERANGE]

Result too large or too small. The result of the function is too large (overflow) or too small (underflow) to be represented in the
available space (defined in the ISO C standard).
[EROFS]

Read-only file system. An attempt was made to modify a file or directory on a file system that is read-only.
[ESOCKTNOSUPPORT]

Socket type not supported. The socket type is not supported by the address family, or the socket type is not supported by the
implementation.
[ESPIPE]

Invalid seek. An attempt was made to access the file offset associated with a pipe or FIFO.
[ESRCH]

No such process. No process can be found corresponding to that specified by the given process ID.
[ESTALE]

Reserved.
[ETIMEDOUT]

Connection timed out. The connection to a remote machine has timed out. If the connection timed out during execution of the
function that reported this error (as opposed to timing out prior to the function being called), it is unspecified whether the
function has completed some or all of the documented behavior associated with a successful completion of the function.

or:

Operation timed out. The time limit associated with the operation was exceeded before the operation completed.

[ETXTBSY]

Text file busy. An attempt was made to execute a pure-procedure program that is currently open for writing, or an attempt has been
made to open for writing a pure-procedure program that is being executed.
[EWOULDBLOCK]

Operation would block. An operation on a socket marked as non-blocking has encountered a situation such as no data available that
otherwise would have caused the function to suspend execution.

A conforming implementation may assign the same values for [EWOULDBLOCK] and [EAGAIN].

[EXDEV]

Improper hard link. Creation of a hard link to a file on another file system was attempted.

2.3.1 Additional Error Numbers

Additional implementation-defined error numbers may be defined in <errno.h>.

2.4 Signal Concepts

2.4.1 Signal Generation and Delivery

A signal is said to be "generated" for (or sent to) a process or thread when the event that causes the signal
first occurs. Examples of such events include detection of hardware faults, timer expiration, signals generated via the
sigevent structure and terminal activity, as well as invocations of the kill()
and sigqueue() functions. In some circumstances, the same event generates signals
for multiple processes.

At the time of generation, a determination shall be made whether the signal has been generated for the process or
for a specific thread within the process. Signals which are generated by some action attributable to a particular thread, such as a
hardware fault, shall be generated for the thread that caused the signal to be generated. Signals that are generated in association
with a process ID or process group ID or an asynchronous event, such as terminal activity, shall be generated for the process.

Each process has an action to be taken in response to each signal defined by the system (see 2.4.3 Signal Actions). A signal is said to be "delivered" to a process when the appropriate action for the
process and signal is taken. A signal is said to be "accepted" by a process when the signal is selected and returned by one of
the sigwait() functions.

During the time between the generation of a signal and its delivery or acceptance, the signal is said to be
"pending". Ordinarily, this interval cannot be detected by an application. However, a signal can be "blocked" from delivery to
a thread. If the action associated with a blocked signal is anything other than to ignore the signal, and if that signal is
generated for the thread, the signal shall remain pending until it is unblocked, it is accepted when it is selected and returned by
a call to the sigwait() function, or the action associated with it is set to ignore
the signal. Signals generated for the process shall be delivered to exactly one of those threads within the process which is in a
call to a sigwait() function selecting that signal or has not blocked delivery of
the signal. If there are no threads in a call to a sigwait() function selecting that
signal, and if all threads within the process block delivery of the signal, the signal shall remain pending on the process until a
thread calls a sigwait() function selecting that signal, a thread unblocks delivery
of the signal, or the action associated with the signal is set to ignore the signal. If the action associated with a blocked signal
is to ignore the signal and if that signal is generated for the process, it is unspecified whether the signal is discarded
immediately upon generation or remains pending.

Each thread has a "signal mask" that defines the set of signals currently blocked from delivery to it. The signal
mask for a thread shall be initialized from that of its parent or creating thread, or from the corresponding thread in the parent
process if the thread was created as the result of a call to fork(). The pthread_sigmask(), sigaction(),
sigprocmask(), and sigsuspend() functions control the manipulation of the signal mask.

The determination of which action is taken in response to a signal is made at the time the signal is delivered,
allowing for any changes since the time of generation. This determination is independent of the means by which the signal was
originally generated. If a subsequent occurrence of a pending signal is generated, it is implementation-defined as to whether the
signal is delivered or accepted more than once in circumstances other than those in which queuing is required. The order in which
multiple, simultaneously pending signals outside the range SIGRTMIN to SIGRTMAX are delivered to or accepted by a process is
unspecified.

When any stop signal (SIGSTOP, SIGTSTP, SIGTTIN, SIGTTOU) is generated for a process or thread, all pending SIGCONT
signals for that process or any of the threads within that process shall be discarded. Conversely, when SIGCONT is generated for a
process or thread, all pending stop signals for that process or any of the threads within that process shall be discarded. When
SIGCONT is generated for a process that is stopped, the process shall be continued, even if the SIGCONT signal is ignored by the
process or is blocked by all threads within the process and there are no threads in a call to a sigwait() function selecting SIGCONT. If SIGCONT is blocked by all threads within the
process, there are no threads in a call to a sigwait() function selecting SIGCONT,
and SIGCONT is not ignored by the process, the SIGCONT signal shall remain pending on the process until it is either unblocked by a
thread or a thread calls a sigwait() function selecting SIGCONT, or a stop signal is
generated for the process or any of the threads within the process.

An implementation shall document any condition not specified by this volume of POSIX.1-2024 under which the
implementation generates signals.

2.4.2 Realtime Signal Generation and Delivery

This section describes functionality to support realtime signal generation and delivery.

Some signal-generating functions, such as high-resolution timer expiration, asynchronous I/O completion,
interprocess message arrival, and the sigqueue() function, support the
specification of an application-defined value, either explicitly as a parameter to the function or in a sigevent structure
parameter. The sigevent structure is defined in <signal.h> and contains
at least the following members:

Member Type

Member Name

Description

int

sigev_notify

Notification type.

int

sigev_signo

Signal number.

union sigval

sigev_value

Signal value.

void(*)(union sigval)

sigev_notify_function

Notification function.

(pthread_attr_t*)

sigev_notify_attributes

Notification attributes.

The sigev_notify member specifies the notification mechanism to use when an asynchronous event occurs. This
volume of POSIX.1-2024 defines the following values for the sigev_notify member:

SIGEV_NONE
No asynchronous notification shall be delivered when the event of interest occurs.
SIGEV_SIGNAL
The signal specified in sigev_signo shall be generated for the process when the event of interest occurs. If the
SA_SIGINFO flag is set for that signal number, then the signal shall be queued to the process and the value specified in
sigev_value shall be the si_value component of the generated signal. If SA_SIGINFO is not set for that signal number,
it is unspecified whether the signal is queued and what value, if any, is sent.
SIGEV_THREAD
A notification function shall be called to perform notification.

An implementation may define additional notification mechanisms.

The sigev_signo member specifies the signal to be generated. The sigev_value member is the
application-defined value to be passed to the signal-catching function at the time of the signal delivery or to be returned at
signal acceptance as the si_value member of the siginfo_t structure.

The sigval union is defined in <signal.h> and contains
at least the following members:

Member Type

Member Name

Description

int

sival_int

Integer signal value.

void*

sival_ptr

Pointer signal value.

The sival_int member shall be used when the application-defined value is of type int; the
sival_ptr member shall be used when the application-defined value is a pointer.

When a signal is generated by the sigqueue() function or any
signal-generating function that supports the specification of an application-defined value, the signal shall be marked pending and,
if the SA_SIGINFO flag is set for that signal, the signal shall be queued to the process along with the application-specified
signal value. Multiple occurrences of signals so generated are queued in FIFO order. It is unspecified whether signals so generated
are queued when the SA_SIGINFO flag is not set for that signal.

Signals generated by the kill() function or other events that cause
signals to occur, such as detection of hardware faults, alarm() timer expiration, or
terminal activity, and for which the implementation does not support queuing, shall have no effect on signals already queued for
the same signal number.

When multiple unblocked signals, all in the range SIGRTMIN to SIGRTMAX, are pending, the behavior shall be as if
the implementation delivers the pending unblocked signal with the lowest signal number within that range. No other ordering of
signal delivery is specified.

If, when a pending signal is delivered, there are additional signals queued to that signal number, the signal shall
remain pending. Otherwise, the pending indication shall be reset.

Multi-threaded programs can use an alternate event notification mechanism. When a notification is processed, and
the sigev_notify member of the sigevent structure has the value SIGEV_THREAD, the function
sigev_notify_function is called with parameter sigev_value.

The function shall be executed in a newly created thread as if it were the start_routine for a call to
pthread_create() with the thread attributes specified by
sigev_notify_attributes. If sigev_notify_attributes is NULL, the behavior shall be as if the thread were created with
the detachstate attribute set to PTHREAD_CREATE_DETACHED. Supplying an attributes structure with a detachstate
attribute of PTHREAD_CREATE_JOINABLE results in undefined behavior. It is implementation-defined whether the signal mask of this
thread has all signals except SIGKILL and SIGSTOP blocked, or is the same as the mask that was in effect for the thread which
installed the sigevent notification handler at the time of the call that installed the handler.

2.4.3 Signal Actions

There are three types of action that can be associated with a signal: SIG_DFL, SIG_IGN, or a pointer to a function.
Initially, all signals shall be set to SIG_DFL or SIG_IGN prior to entry of the main() routine (see the exec functions). The actions prescribed by these values are as follows.

SIG_DFL

Signal-specific default action.

The default actions for the signals defined in this volume of POSIX.1-2024 are specified under <signal.h>. The default actions for the realtime signals in the range SIGRTMIN to
SIGRTMAX shall be to terminate the process abnormally.

If the default action is to terminate the process abnormally, the process is terminated as if by a call to _exit(), except that the status made available to wait(), waitid(), and waitpid() indicates abnormal termination by the signal. If the default action is to
terminate the process abnormally with additional actions, implementation-defined abnormal termination actions, such as creation of
a core image, may also occur.

If the default action is to stop the process, the execution of that process is temporarily suspended. When a
process stops, a SIGCHLD signal shall be generated for its parent process, unless the parent process has set the SA_NOCLDSTOP flag.
While a process is stopped, any additional signals that are sent to the process shall not be delivered until the process is
continued, except SIGKILL which always terminates the receiving process. A process that is a member of an orphaned process group
shall not be allowed to stop in response to the SIGTSTP, SIGTTIN, or SIGTTOU signals. In cases where delivery of one of these
signals would stop such a process, the signal shall be discarded.

If the default action is to ignore the signal, delivery of the signal shall have no effect on the process.

Setting a signal action to SIG_DFL for a signal that is pending, and whose default action is to ignore the signal
(for example, SIGCHLD), shall cause the pending signal to be discarded, whether or not it is blocked. Any queued values pending
shall be discarded and the resources used to queue them shall be released and returned to the system for other use.

The default action for SIGCONT is to resume execution at the point where the process was stopped, after first
handling any pending unblocked signals.

[XSI]  When a stopped process is continued, a SIGCHLD signal may be generated for its parent process, unless the parent
process has set the SA_NOCLDSTOP flag.

SIG_IGN

Ignore signal.

Delivery of the signal shall have no effect on the process. The behavior of a process is undefined after it ignores
a SIGFPE, SIGILL, SIGSEGV, or SIGBUS signal that was not generated by kill(), sigqueue(), or raise().

The system shall not allow the action for the signals SIGKILL or SIGSTOP to be set to SIG_IGN.

Setting a signal action to SIG_IGN for a signal that is pending shall cause the pending signal to be discarded,
whether or not it is blocked.

If a process sets the action for the SIGCHLD signal to SIG_IGN, the behavior is unspecified,

[XSI]
except as specified under "Consequences of Process Termination" in the description of the _Exit() function (see XSH _Exit()).

Any queued values pending shall be discarded and the resources used to queue them shall be released and made
available to queue other signals.

Pointer to a Function

Catch signal.

On delivery of the signal, the receiving process is to execute the signal-catching function at the specified
address. After returning from the signal-catching function, the receiving process shall resume execution at the point at which it
was interrupted.

If the SA_SIGINFO flag for the signal is cleared, the signal-catching function shall be entered as a C-language
function call as follows:

void func(int signo);

If the SA_SIGINFO flag for the signal is set, the signal-catching function shall be entered as a C-language
function call as follows:

void func(int signo, siginfo_t *info, void *context);

where func is the specified signal-catching function, signo is the signal number of the signal being
delivered, and info is a pointer to a siginfo_t structure defined in <signal.h> containing at least the following members:

Member Type

Member Name

Description

int

si_signo

Signal number.

int

si_code

Cause of the signal.

pid_t

si_pid

Sending process ID.

uid_t

si_uid

Real user ID of sending process.

void *

si_addr

Address of faulting instruction.

int

si_status

Exit value or signal.

union sigval

si_value

Signal value.

The si_signo member shall contain the signal number. This shall be the same as the signo parameter.
The si_code member shall contain a code identifying the cause of the signal. The following non-signal-specific values are
defined for si_code:

SI_USER
The signal was sent by the kill() function. The implementation may set
si_code to SI_USER if the signal was sent by the raise() or abort() functions or any similar functions provided as implementation extensions.
SI_QUEUE
The signal was sent by the sigqueue() function.
SI_TIMER
The signal was generated by the expiration of a timer set by timer_settime().
SI_ASYNCIO
The signal was generated by the completion of an asynchronous I/O request.
SI_MESGQ
[MSG]
The signal was generated by the arrival of a message on an empty message queue.

Signal-specific values for si_code are also defined, as described in XBD <signal.h>.

If the signal was not generated by one of the functions or events listed above, si_code shall be set either
to one of the signal-specific values described in XBD <signal.h>, or to an
implementation-defined value that is not equal to any of the values defined above.

If si_code is SI_USER or SI_QUEUE, [XSI]   or any value less than or equal to 0,   then the signal was generated by a process and si_pid and
si_uid shall be set to the process ID and the real user ID of the sender, respectively.

In addition, si_addr, si_pid, si_status, and si_uid shall be set for certain
signal-specific values of si_code, as described in XBD <signal.h>.

If si_code is one of SI_QUEUE, SI_TIMER, SI_ASYNCIO, or SI_MESGQ, then si_value shall contain the
application-specified signal value. Otherwise, the contents of si_value are undefined.

The behavior of a process is undefined after it returns normally from a signal-catching function for a SIGBUS,
SIGFPE, SIGILL, or SIGSEGV signal that was not generated by kill(), sigqueue(), or raise().

The system shall not allow a process to catch the signals SIGKILL and SIGSTOP.

If a process establishes a signal-catching function for the SIGCHLD signal while it has a terminated child process
for which it has not waited, it is unspecified whether a SIGCHLD signal is generated to indicate that child process.

If the process is multi-threaded, or if the process is single-threaded and a signal handler is executed other than
as the result of:

The process calling abort(), raise(), kill(), pthread_kill(), or sigqueue() to
generate a signal that is not blocked

A pending signal being unblocked and being delivered before the call that unblocked it returns

the behavior is undefined if:

The signal handler refers to any object other than errno with static or thread storage duration that is not
a lock-free atomic object, and not a non-modifiable object (for example, string literals, objects that were defined with a
const-qualified type, and objects in memory that is mapped read-only), other than by assigning a value to an object declared as
volatile sig_atomic_t, unless the previous modification (if any) to the object happens before the signal handler is called
and the return from the signal handler happens before the next modification (if any) to the object.

The signal handler calls any function or function-like macro defined in this standard other than one of the
functions and macros specified below as being async-signal-safe.

The following table defines a set of functions and function-like macros that shall be async-signal-safe. Therefore,
applications can call them, without restriction, from signal-catching functions. Note that, although there is no restriction on the
calls themselves, for certain functions there are restrictions on subsequent behavior after the function is called from a
signal-catching function (see longjmp()).

_Exit()

_Fork()

_exit()

abort()

accept()

accept4()

access()

aio_error()

aio_return()

aio_suspend()

alarm()

be16toh()

be32toh()

be64toh()

bind()

cfgetispeed()

cfgetospeed()

cfsetispeed()

cfsetospeed()

chdir()

chmod()

chown()

clock_gettime()

close()

connect()

creat()

dup()

dup2()

dup3()

execl()

execle()

execv()

execve()

faccessat()

fchdir()

fchmod()

fchmodat()

fchown()

fchownat()

fcntl()

fdatasync()

fexecve()

ffs()

fstat()

fstatat()

fsync()

ftruncate()

futimens()

getegid()

geteuid()

getgid()

getgroups()

getpeername()

getpgrp()

getpid()

getppid()

getresgid()

getresuid()

getsockname()

getsockopt()

getuid()

htobe16()

htobe32()

htobe64()

htole16()

htole32()

htole64()

htonl()

htons()

kill()

killpg()

le16toh()

le32toh()

le64toh()

link()

linkat()

listen()

longjmp()

lseek()

lstat()

memccpy()

memchr()

memcmp()

memcpy()

memmove()

memset()

mkdir()

mkdirat()

mkfifo()

mkfifoat()

mknod()

mknodat()

ntohl()

ntohs()

open()

openat()

pause()

pipe()

pipe2()

poll()

posix_close()

ppoll()

pread()

pselect()

pthread_kill()

pthread_self()

pthread_setcancelstate()

pthread_sigmask()

pwrite()

quick_exit()

raise()

read()

readv()

readlink()

readlinkat()

recv()

recvfrom()

recvmsg()

rename()

renameat()

rmdir()

select()

sem_post()

send()

sendmsg()

sendto()

setegid()

seteuid()

setgid()

setpgid()

setregid()

setresgid()

setresuid()

setreuid()

setsid()

setsockopt()

setuid()

shutdown()

sig2str()

sigaction()

sigaddset()

sigdelset()

sigemptyset()

sigfillset()

sigismember()

siglongjmp()

signal()

sigpending()

sigprocmask()

sigqueue()

sigsuspend()

sleep()

sockatmark()

socket()

socketpair()

stat()

stpcpy()

stpncpy()

strcat()

strchr()

strcmp()

strcpy()

strcspn()

strlcat()

strlcpy()

strlen()

strncat()

strncmp()

strncpy()

strnlen()

strpbrk()

strrchr()

strspn()

strstr()

strtok_r()

symlink()

symlinkat()

tcdrain()

tcflow()

tcflush()

tcgetattr()

tcgetpgrp()

tcgetwinsize()

tcsendbreak()

tcsetattr()

tcsetpgrp()

tcsetwinsize()

time()

timer_getoverrun()

timer_gettime()

timer_settime()

times()

umask()

uname()

unlink()

unlinkat()

utimensat()

utimes()

va_arg()

va_copy()

va_end()

va_start()

wait()

waitid()

waitpid()

wcpcpy()

wcpncpy()

wcscat()

wcschr()

wcscmp()

wcscpy()

wcscspn()

wcslcat()

wcslcpy()

wcslen()

wcsncat()

wcsncmp()

wcsncpy()

wcsnlen()

wcspbrk()

wcsrchr()

wcsspn()

wcsstr()

wcstok()

wmemchr()

wmemcmp()

wmemcpy()

wmemmove()

wmemset()

write()

writev()

In addition, the functions in <stdatomic.h> other than
atomic_init() shall be async-signal-safe when the atomic arguments are
lock-free, and the atomic_is_lock_free() function shall be
async-signal-safe when called with an atomic argument.

All other functions (including generic functions) and function-like macros may be unsafe with respect to signals.
It is implementation-defined which additional interfaces, if any, are also async-signal-safe. In the presence of signals, all
functions defined by this volume of POSIX.1-2024 shall behave as defined when called from or interrupted by a signal-catching
function, with the exception that when a signal interrupts an unsafe function or function-like macro, or equivalent (such as the
processing equivalent to exit() performed after a return from the initial call to
main()), and the signal-catching function calls an unsafe function or function-like macro, the behavior is undefined.
Additional exceptions are specified in the descriptions of individual functions such as longjmp().

Operations which obtain the value of errno and operations which assign a value to errno shall be
async-signal-safe, provided that the signal-catching function saves the value of errno upon entry and restores it before it
returns.

When a signal is delivered to a thread, if the action of that signal specifies termination, stop, or continue, the
entire process shall be terminated, stopped, or continued, respectively.

2.4.4 Signal Effects on Other Functions

Signals affect the behavior of certain functions defined by this volume of POSIX.1-2024 if delivered to a process
while it is executing such a function. If the action of the signal is to terminate the process, the process shall be terminated and
the function shall not return. If the action of the signal is to stop the process, the process shall stop until continued or
terminated. Generation of a SIGCONT signal for the process shall cause the process to be continued, and the original function shall
continue at the point the process was stopped. If the action of the signal is to invoke a signal-catching function, the
signal-catching function shall be invoked; in this case the original function is said to be "interrupted" by the signal. If the
signal-catching function executes a return statement, the behavior of the interrupted function shall be as described
individually for that function, except as noted for unsafe functions. After returning from a signal-catching function, the value of
errno is unspecified if the signal-catching function or any function it called assigned a value to errno and the
signal-catching function did not save and restore the original value of errno. Signals that are ignored shall not affect the
behavior of any function; signals that are blocked shall not affect the behavior of any function until they are unblocked and then
delivered, except as specified for the sigpending() and sigwait() functions.

2.5 Standard I/O Streams

A stream is associated with an external file (which may be a physical device) [CX]   or memory
buffer   by "opening" a file [CX]   or buffer.
This may involve "creating" a new file. Creating an existing file
causes its former contents to be discarded if necessary. If a file can support positioning requests (such as a disk file, as
opposed to a terminal), then a "file position indicator" associated with the stream is positioned at the start (byte number 0) of
the file, unless the file is opened with append mode, in which case it is implementation-defined whether the file position
indicator is initially positioned at the beginning or end of the file. The file position indicator is maintained by subsequent
reads, writes, and positioning requests, to facilitate an orderly progression through the file.

The wide-character input functions shall read characters from the stream and convert them to wide characters as if
they were read by successive calls to the fgetwc() function. Each conversion shall
occur as if by a call to the mbrtowc() function, with the conversion state described
by the stream's own mbstate_t object (see 2.5.2 Stream Orientation and Encoding Rules). The
byte input functions shall read characters from the stream as if by successive calls to the fgetc() function.

The wide-character output functions shall convert wide characters to characters and write them to the stream as if
they were written by successive calls to the fputwc() function. Each conversion shall
occur as if by a call to the wcrtomb() function, with the conversion state described
by the stream's own mbstate_t object (see 2.5.2 Stream Orientation and Encoding Rules). The
byte output functions shall write characters to the stream as if by successive calls to the fputc() function.

The perror(), psiginfo(), and psignal() functions shall
behave as described above for the byte output functions if the stream is already byte-oriented, and shall behave as described above
for the wide-character output functions if the stream is already wide-oriented. If the stream has no orientation, they shall behave
as described for the byte output functions except that they shall not change the orientation of the stream.

Functions other than perror(), psiginfo(), and psignal() that write to
streams but are neither wide-character output nor byte output functions (getopt() and
wordexp()), shall behave as described above for the byte output functions, except
that if the stream has no orientation, it is unspecified whether they set the stream to byte orientation or leave it with no
orientation.

When a stream is "unbuffered", bytes are intended to appear from the source or at the destination as soon as
possible; otherwise, bytes may be accumulated and transmitted as a block. When a stream is "fully buffered", bytes are intended
to be transmitted as a block when a buffer is filled. When a stream is "line buffered", bytes are intended to be transmitted as a
block when a <newline> byte is encountered. Furthermore, bytes are intended to be transmitted as a block when a buffer is
filled, when input is requested on an unbuffered stream, or when input is requested on a line-buffered stream that requires the
transmission of bytes. Support for these characteristics is implementation-defined, and may be affected via setbuf() and setvbuf().

A file may be disassociated from a controlling stream by "closing" the file. Output streams are flushed (any
unwritten buffer contents are transmitted) before the stream is disassociated from the file. The value of a pointer to a
FILE object is unspecified after the associated file is closed (including the standard streams).

A file may be subsequently reopened, by the same or another program execution, and its contents reclaimed or
modified (if it can be repositioned at its start). If the main() function returns to its original caller, or if the exit() function is called, all open files are closed (hence all output streams are flushed)
before program termination. Other paths to program termination, such as calling abort(), need not close all files properly.

The address of the FILE object used to control a stream may be significant; a copy of a FILE object
need not necessarily serve in place of the original.

At program start-up, three streams shall be predefined and already open: stdin (standard input, for
conventional input) for reading, stdout (standard output, for conventional output) for writing, and stderr (standard
error, for diagnostic output) for writing. When opened, stderr shall not be fully buffered; stdin and stdout
shall be fully buffered if and only if [CX]   the file descriptor associated with the stream is determined not to be associated with an
interactive device.

Each stream shall have an associated lock that is used to prevent data races when multiple threads of execution
access a stream, and to restrict the interleaving of stream operations performed by multiple threads. Only one thread can hold this
lock at a time. The lock shall be reentrant: a single thread can hold the lock multiple times at a given time. All functions that
read, write, position, or query the position of a stream, [CX]   except those with names ending _unlocked,   shall lock the stream [CX]   as if by a
call to flockfile()   before accessing it and release the lock [CX]   as if by a call to funlockfile()   when
the access is complete.

[CX]  If the lock is not immediately available, the function shall wait for it to become available, except in the following
circumstances. If the stream is line buffered and is open for writing or for update, and the reason the function is attempting to
lock the stream is because it is going to request input on another stream that is unbuffered, or is line buffered and requires the
transmission of characters from the host environment (see above), then the function shall attempt to determine whether a deadlock
situation exists. If a deadlock situation is found to exist, the function shall fail. If the function is able to establish that a
deadlock situation does not exist, it shall wait for the lock to become available. If the function does not establish whether or
not a deadlock situation exists, it shall continue as if it had already locked the stream, found its buffer to be empty, and
released the lock.

[CX]  A stream associated with a memory buffer shall have the same operations for text files that a stream associated with an
external file would have. In addition, the stream orientation shall be determined in exactly the same fashion.

Input and output operations on a stream associated with a memory buffer by a call to fmemopen() shall be constrained by the implementation to take place within the bounds of
the memory buffer. In the case of a stream opened by open_memstream() or
open_wmemstream(), the memory area shall grow dynamically to accommodate
write operations as necessary. For output, if the stream is fully buffered or line buffered, data shall be moved from the stream's
internal buffer, or a buffer provided by setvbuf(), to the memory buffer during a
flush or close operation. For input, it is unspecified whether a buffer provided by setvbuf() is used or whether read operations read directly from the memory buffer provided
to or allocated by fmemopen().

When a standard I/O stream has an associated memory buffer (whether allocated internally, supplied to setvbuf(), or supplied to fmemopen()), the
behavior is undefined if that buffer overlaps with the destination buffer passed to a call that reads from the stream or with the
source buffer passed to a call that writes to the stream.

2.5.1 Interaction of File Descriptors and Standard I/O Streams

[CX]  This section describes the interaction of file descriptors and standard I/O streams. The functionality described in
this section is an extension to the ISO C standard (and the rest of this section is not further CX shaded).

An open file description may be accessed through a file descriptor, which is created using functions such as
open() or pipe(), or through a stream,
which is created using functions such as fopen() or popen(). Either a file descriptor or a stream is called a "handle" on the open file
description to which it refers; an open file description may have several handles.

Handles can be created or destroyed by explicit user action, without affecting the underlying open file
description. Some of the ways to create them include fcntl(), dup(), fdopen(), fileno(), and fork(). They can be destroyed by at
least fclose(), close(), and the
exec functions.

A file descriptor that is never used in an operation that could affect the file offset (for example, read(), write(), or lseek()) is not considered a handle for this discussion, but could give rise to one (for
example, as a consequence of fdopen(), dup(), or fork()). This exception does not include
the file descriptor underlying a stream, whether created with fopen() or fdopen(), so long as it is not used directly by the application to affect the file offset.
The read() and write() functions
implicitly affect the file offset; lseek() explicitly affects it.

The result of function calls involving any one handle (the "active handle") is defined elsewhere in this volume
of POSIX.1-2024, but if two or more handles are used, and any one of them is a stream, the application shall ensure that their
actions are coordinated as described below. If this is not done, the result is undefined.

A handle which is a stream is considered to be closed when either an fclose(), or freopen() with non-null filename,
is executed on it (for freopen() with a null filename, it is implementation-defined
whether a new handle is created or the existing one reused), or when the process owning that stream terminates with exit(), abort(), or due to a signal. Several
functions close file descriptors, including close(), dup2(), _exit(), the exec functions when FD_CLOEXEC is set on a file descriptor, fork() when FD_CLOFORK is set on a file descriptor, and posix_spawn() when either FD_CLOEXEC or FD_CLOFORK is set.

For a handle to become the active handle, the application shall ensure that the actions below are performed between
the last use of the handle (the current active handle) and the first use of the second handle (the future active handle). The
second handle then becomes the active handle. All activity by the application affecting the file offset on the first handle shall
be suspended until it again becomes the active file handle. (If a stream function has as an underlying function one that affects
the file offset, the stream function shall be considered to affect the file offset.)

The handles need not be in the same process for these rules to apply.

Note that after a fork(), two handles exist where one existed before.
The application shall ensure that, if both handles can ever be accessed, they are both in a state where the other could become the
active handle first. The application shall prepare for a fork() exactly as if it were a
change of active handle. (If the only action performed by one of the processes is one of the exec functions or _exit() (not exit()), the handle is never accessed in that process.)

For the first handle, the first applicable condition below applies. After the actions required below are taken, if
the handle is still open, the application can close it.

If it is a file descriptor, no action is required.

If the only further action to be performed on any handle to this open file descriptor is to close it, no action
need be taken.

If it is a stream which is unbuffered, no action need be taken.

If it is a stream which is line buffered, and the last byte written to the stream was a <newline> (that is,
as if a:

putc('\n')

was the most recent operation on that stream), no action need be taken.

If it is a stream which is open for writing or appending (but not also open for reading), the application shall
either perform an fflush(), or the stream shall be closed.

If the stream is open for reading and it is at the end of the file (feof() is true), no action need be taken.

If the stream is open with a mode that allows reading and the underlying open file description refers to a device
that is capable of seeking, the application shall either perform an fflush(), or the
stream shall be closed.

For the second handle:

If any previous active handle has been used by a function that explicitly changed the file offset, except as
required above for the first handle, the application shall perform an lseek() or
fseek() (as appropriate to the type of handle) to an appropriate location.

If the active handle ceases to be accessible before the requirements on the first handle, above, have been met, the
state of the open file description becomes undefined. This might occur during functions such as a fork() or _exit().

The exec functions make inaccessible all streams that are open at the
time they are called, independent of which streams or file descriptors may be available to the new process image.

When these rules are followed, regardless of the sequence of handles used, no data shall be lost or duplicated when
writing, and all data shall be written in order, except as requested by seeks. It is implementation-defined whether, and under what
conditions, all input is seen exactly once.

Each function that operates on a stream is said to have zero or more "underlying functions". This means that the
stream function shares certain traits with the underlying functions, but does not require that there be any relation between the
implementations of the stream function and its underlying functions.

2.5.2 Stream Orientation and Encoding Rules

The definition of a stream includes an "orientation". After a stream is associated with an external file, but
before any operations are performed on it, the stream is without orientation. Once a wide-character input/output function has been
applied to a stream without orientation, the stream shall become "wide-oriented". Similarly, once a byte input/output function
has been applied to a stream without orientation, the stream shall become "byte-oriented". Only a call to the freopen() function or the fwide() function can
otherwise alter the orientation of a stream.

A successful call to freopen() shall remove any orientation. The
three predefined streams standard input, standard output, and standard error shall be unoriented at program
start-up.

Byte input/output functions cannot be applied to a wide-oriented stream, and wide-character input/output functions
cannot be applied to a byte-oriented stream. The remaining stream operations shall not affect and shall not be affected by a
stream's orientation, except for the following additional restriction:

For wide-oriented streams, after a successful call to a file-positioning function that leaves the file position
indicator prior to the end-of-file, a wide-character output function can overwrite a partial character; any file contents beyond
the byte(s) written are henceforth undefined.

Each wide-oriented stream [CX]   that was not opened with open_wmemstream()
has an associated mbstate_t object that stores the current parse state of the stream. A successful call to fgetpos() shall store a representation of the value of this mbstate_t object as part
of the value of the fpos_t object. A later successful call to fsetpos() using
the same stored fpos_t value shall restore the value of the associated mbstate_t object as well as the position
within the controlled stream.

Implementations that support multiple encoding rules associate an encoding rule with the stream. The encoding rule
shall be determined by the setting of the LC_CTYPE category in the current locale at the time when the stream becomes
wide-oriented. As with the stream's orientation, the encoding rule associated with a stream cannot be changed once it has been set,
except by a successful call to freopen() which clears the encoding rule and resets
the orientation to unoriented.

Although wide-oriented streams are conceptually sequences of wide characters, the external file associated with a
wide-oriented stream [CX]   that was not opened with open_wmemstream()  is
a sequence of (possibly multi-byte) characters generalized as follows:

Multi-byte encodings within files may contain embedded null bytes (unlike multi-byte encodings valid for use
internal to the program).

A file need not begin nor end in the initial shift state.

Moreover, the encodings used for characters may differ among files. Both the nature and choice of such encodings
are implementation-defined.

[CX]  On streams that were not opened with open_wmemstream(),
the wide-character input functions read characters from the stream
and convert them to wide characters as if they were read by successive calls to the fgetwc() function. Each conversion shall occur as if by a call to the mbrtowc() function, with the conversion state described by the stream's own mbstate_t
object, [CX]   except the encoding rule associated with the stream is used instead of the encoding rule implied by the LC_CTYPE
category of the current locale.

[CX]  On streams that were not opened with open_wmemstream(),
the wide-character output functions convert wide characters to
(possibly multi-byte) characters and write them to the stream as if they were written by successive calls to the fputwc() function. Each conversion shall occur as if by a call to the wcrtomb() function, with the conversion state described by the stream's own mbstate_t
object, [CX]   except the encoding rule associated with the stream is used instead of the encoding rule implied by the LC_CTYPE
category of the current locale.

An "encoding error" shall occur if the character sequence presented to the underlying mbrtowc() function does not form a valid (generalized) character, or if the code value
passed to the underlying wcrtomb() function does not correspond to a valid
(generalized) character. The wide-character input/output functions and the byte input/output functions store the value of the macro
[EILSEQ] in errno if and only if an encoding error occurs.

2.6 File Descriptor Allocation

All functions that open one or more file descriptors shall, unless specified otherwise, atomically allocate the
lowest numbered available (that is, not already open in the calling process) file descriptor at the time of each allocation. Where
a single function allocates two file descriptors (for example, pipe() or socketpair()), the allocations may be independent and therefore applications should not
expect them to have adjacent values or depend on which has the higher value.

2.7 XSI Interprocess Communication

[XSI]  This section describes extensions to support interprocess communication. The functionality described in this section
shall be provided on implementations that support the XSI option (and the rest of this section is not further marked).

The following message passing, semaphore, and shared memory services form an XSI interprocess communication
facility. Certain aspects of their operation are common, and are defined as follows.

IPC Functions

msgctl()

msgget()

msgrcv()

msgsnd()

semctl()

semget()

semop()

shmat()

shmctl()

shmdt()

shmget()

Another interprocess communication facility is provided by functions in the Realtime Option Group; see 2.8 Realtime.

2.7.1 IPC General Description

Each individual shared memory segment, message queue, and semaphore set shall be identified by a unique positive
integer, called, respectively, a shared memory identifier, shmid, a semaphore identifier, semid, and a message queue
identifier, msqid. The identifiers shall be returned by calls to shmget(),
semget(), and msgget(),
respectively.

Associated with each identifier is a data structure which contains data related to the operations which may be or
may have been performed; see the Base Definitions volume of POSIX.1-2024, <sys/shm.h>, <sys/sem.h>, and
<sys/msg.h> for their descriptions.

Each of the data structures contains both ownership information and an ipc_perm structure (see the Base
Definitions volume of POSIX.1-2024, <sys/ipc.h>) which are used in
conjunction to determine whether or not read/write (read/alter for semaphores) permissions should be granted to processes using the
IPC facilities. The mode member of the ipc_perm structure acts as a bit field which determines the permissions.

The values of the bits are given below in octal notation along with the symbolic constants defined in <sys/stat.h> that can be used to represent them.

Octal Value

<sys/stat.h> Symbolic Constant

Meaning

0400

S_IRUSR

Read by user.

0200

S_IWUSR

Write (for shared memory & message queues) or alter (for semaphores) by user.

0040

S_IRGRP

Read by group.

0020

S_IWGRP

Write or alter by group.

0004

S_IROTH

Read by others.

0002

S_IWOTH

Write or alter by others.

The name of the ipc_perm structure is shm_perm, sem_perm, or msg_perm, depending on
which service is being used. In each case, read and write/alter permissions shall be granted to a process if one or more of the
following are true ("xxx" is replaced by shm, sem, or msg, as appropriate):

The process has appropriate privileges.

The effective user ID of the process matches xxx_perm.cuid or xxx_perm.uid in the data structure
associated with the IPC identifier, and the appropriate bit of the user field in xxx_perm.mode is set.

The effective user ID of the process does not match xxx_perm.cuid or xxx_perm.uid but the effective
group ID of the process matches xxx_perm.cgid or xxx_perm.gid in the data structure associated with the IPC
identifier, and the appropriate bit of the group field in xxx_perm.mode is set.

The effective user ID of the process does not match xxx_perm.cuid or xxx_perm.uid and the effective
group ID of the process does not match xxx_perm.cgid or xxx_perm.gid in the data structure associated with the IPC
identifier, but the appropriate bit of the other field in xxx_perm.mode is set.

Otherwise, the permission shall be denied.

In addition to the ipc_perm structure, each associated data structure includes several time_t fields
for recording timestamps of particular operations. When an operation is described as setting a timestamp to the current time, that
particular timestamp member of the associated data structure shall be set to the largest time_t value which is not greater
than the current time.

2.8 Realtime

This section defines functions to support the source portability of applications with realtime requirements. The
presence of some of these functions is dependent on support for implementation options described in the text.

The specific functional areas included in this section and their scope include the following. Full definitions of
these terms can be found in XBD 3. Definitions.

Semaphores

Process Memory Locking

Memory Mapped Files and Shared Memory Objects

Priority Scheduling

Realtime Signal Extension

Timers

Interprocess Communication

Synchronized Input and Output

Asynchronous Input and Output

All the realtime functions defined in this volume of POSIX.1-2024 are portable, although some of the numeric
parameters used by an implementation may have hardware dependencies.

2.8.1 Realtime Signals

See 2.4.2 Realtime Signal Generation and Delivery.

2.8.2 Asynchronous I/O

An asynchronous I/O control block structure aiocb is used in many asynchronous I/O functions. It is defined
in the Base Definitions volume of POSIX.1-2024, <aio.h> and has at least the
following members:

Member Type

Member Name

Description

int

aio_fildes

File descriptor.

off_t

aio_offset

File offset.

volatile void*

aio_buf

Location of buffer.

size_t

aio_nbytes

Length of transfer.

int

aio_reqprio

Request priority offset.

struct sigevent

aio_sigevent

Signal number and value.

int

aio_lio_opcode

Operation to be performed.

The aio_fildes element is the file descriptor on which the asynchronous operation is performed.

If O_APPEND is not set for the file descriptor aio_fildes and if aio_fildes is associated with a
device that is capable of seeking, then the requested operation takes place at the absolute position in the file as given by
aio_offset, as if lseek() were called immediately prior to the operation with
an offset argument equal to aio_offset and a whence argument equal to SEEK_SET. If O_APPEND is set for the
file descriptor, or if aio_fildes is associated with a device that is incapable of seeking, write operations append to the
file in the same order as the calls were made, with the following exception: under implementation-defined circumstances, such as
operation on a multi-processor or when requests of differing priorities are submitted at the same time, the ordering restriction
may be relaxed. Since there is no way for a strictly conforming application to determine whether this relaxation applies, all
strictly conforming applications which rely on ordering of output shall be written in such a way that they operate correctly if the
relaxation applies. After a successful call to enqueue an asynchronous I/O operation, the value of the file offset for the file is
unspecified. The aio_nbytes and aio_buf elements are the same as the nbyte and buf arguments defined by
read() and write(), respectively.

If _POSIX_PRIORITIZED_IO and _POSIX_PRIORITY_SCHEDULING are defined, then asynchronous I/O is queued in priority
order, with the priority of each asynchronous operation based on the current scheduling priority of the calling process. The
aio_reqprio member can be used to lower (but not raise) the asynchronous I/O operation priority and is within the range zero
through {AIO_PRIO_DELTA_MAX}, inclusive. Unless both _POSIX_PRIORITIZED_IO and _POSIX_PRIORITY_SCHEDULING are defined, the order of
processing asynchronous I/O requests is unspecified. When both _POSIX_PRIORITIZED_IO and _POSIX_PRIORITY_SCHEDULING are defined,
the order of processing of requests submitted by processes whose schedulers are not SCHED_FIFO, SCHED_RR, or SCHED_SPORADIC is
unspecified. The priority of an asynchronous request is computed as (process scheduling priority) minus aio_reqprio. The
priority assigned to each asynchronous I/O request is an indication of the desired order of execution of the request relative to
other asynchronous I/O requests for this file. If _POSIX_PRIORITIZED_IO is defined, requests issued with the same priority to a
character special file are processed by the underlying device in FIFO order; the order of processing of requests of the same
priority issued to files that are not character special files is unspecified. Numerically higher priority values indicate requests
of higher priority. The value of aio_reqprio has no effect on process scheduling priority. When prioritized asynchronous I/O
requests to the same file are blocked waiting for a resource required for that I/O operation, the higher-priority I/O requests
shall be granted the resource before lower-priority I/O requests are granted the resource. The relative priority of asynchronous
I/O and synchronous I/O is implementation-defined. If _POSIX_PRIORITIZED_IO is defined, the implementation shall define for which
files I/O prioritization is supported.

The aio_sigevent determines how the calling process shall be notified upon I/O completion, as specified in
2.4.1 Signal Generation and Delivery. If aio_sigevent.sigev_notify is SIGEV_NONE, then no
signal shall be posted upon I/O completion, but the error status for the operation and the return status for the operation shall be
set appropriately.

The aio_lio_opcode field is used only by the lio_listio()
call. The lio_listio() call allows multiple asynchronous I/O operations to be
submitted at a single time. The function takes as an argument an array of pointers to aiocb structures. Each aiocb
structure indicates the operation to be performed (read or write) via the aio_lio_opcode field.

The address of the aiocb structure is used as a handle for retrieving the error status and return status of
the asynchronous operation while it is in progress.

The aiocb structure and the data buffers associated with the asynchronous I/O operation are being used by
the system for asynchronous I/O while, and only while, the error status of the asynchronous operation is equal to [EINPROGRESS].
Applications shall not modify the aiocb structure while the structure is being used by the system for asynchronous I/O.

The return status of the asynchronous operation is the number of bytes transferred by the I/O operation. If the
error status is set to indicate an error completion, then the return status is set to the return value that the corresponding
read(), write(), or fsync() call would have returned. When the error status is not equal to [EINPROGRESS], the
return status shall reflect the return status of the corresponding synchronous operation.

2.8.3 Memory Management

2.8.3.1 Memory Locking

[MLR]  Range memory locking operations are defined in terms of pages. Implementations may restrict the size and alignment of
range lockings to be on page-size boundaries. The page size, in bytes, is the value of the configurable system variable {PAGESIZE}.
If an implementation has no restrictions on size or alignment, it may specify a 1-byte page size.

[ML|MLR]  Memory locking guarantees the residence of portions of the address space. It is implementation-defined
whether locking memory guarantees fixed translation between virtual addresses (as seen by the process) and physical addresses.
Per-process memory locks are not inherited across a fork(), and all memory locks owned
by a process are unlocked upon exec or process termination. Unmapping of an address
range removes any memory locks established on that address range by this process.

2.8.3.2 Memory Mapped Files

Range memory mapping operations are defined in terms of pages. Implementations may restrict the size and alignment
of range mappings to be on page-size boundaries. The page size, in bytes, is the value of the configurable system variable
{PAGESIZE}. If an implementation has no restrictions on size or alignment, it may specify a 1-byte page size.

Memory mapped files provide a mechanism that allows a process to access files by directly incorporating file data
into its address space. Once a file is mapped into a process address space, the data can be manipulated as memory. If more than one
process maps a file, its contents are shared among them. If the mappings allow shared write access, then data written into the
memory object through the address space of one process appears in the address spaces of all processes that similarly map the same
portion of the memory object.

[SHM]  Shared memory objects are named regions of storage that may be independent of the file system and can be mapped into
the address space of one or more processes to allow them to share the associated memory.

An unlink() of a file [SHM]   or shm_unlink() of a shared memory object,  while causing the removal of the name, does not unmap any mappings established for the object. Once the
name has been removed, the contents of the memory object are preserved as long as it is referenced. The memory object remains
referenced as long as a process has the memory object open or has some area of the memory object mapped.

2.8.3.3 Memory Protection

When an object is mapped, various application accesses to the mapped region may result in signals. In this context,
SIGBUS is used to indicate an error using the mapped object, and SIGSEGV is used to indicate a protection violation or misuse of an
address:

A mapping may be restricted to disallow some types of access.

Write attempts to memory that was mapped without write access, or any access to memory mapped PROT_NONE, shall
result in a SIGSEGV signal.

References to unmapped addresses shall result in a SIGSEGV signal.

Reference to whole pages within the mapping, but beyond the current length of the object, shall result in a SIGBUS
signal.

The size of the object is unaffected by access beyond the end of the object (even if a SIGBUS is not
generated).

2.8.3.4 Typed Memory Objects

[TYM]  The functionality described in this section shall be provided on implementations that support the Typed Memory Objects
option (and the rest of this section is not further marked for this option).

Implementations may support the Typed Memory Objects option independently of support for memory mapped files or
shared memory objects. Typed memory objects are implementation-configurable named storage pools accessible from one or more
processors in a system, each via one or more ports, such as backplane buses, LANs, I/O channels, and so on. Each valid combination
of a storage pool and a port is identified through a name that is defined at system configuration time, in an
implementation-defined manner; the name may be independent of the file system. Using this name, a typed memory object can be opened
and mapped into process address space. For a given storage pool and port, it is necessary to support both dynamic allocation from
the pool as well as mapping at an application-supplied offset within the pool; when dynamic allocation has been performed,
subsequent deallocation shall be supported. Lastly, accessing typed memory objects from different ports requires a method for
obtaining the offset and length of contiguous storage of a region of typed memory (dynamically allocated or not); this allows typed
memory to be shared among processes and/or processors while being accessed from the desired port.

2.8.4 Process Scheduling

[PS]  The functionality described in this section shall be provided on implementations that support the Process Scheduling
option (and the rest of this section is not further marked for this option).

Scheduling Policies

The scheduling semantics described in this volume of POSIX.1-2024 are defined in terms of a conceptual model that
contains a set of thread lists. No implementation structures are necessarily implied by the use of this conceptual model. It is
assumed that no time elapses during operations described using this model, and therefore no simultaneous operations are possible.
This model discusses only processor scheduling for runnable threads, but it should be noted that greatly enhanced predictability of
realtime applications results if the sequencing of other resources takes processor scheduling policy into account.

There is, conceptually, one thread list for each priority. A runnable thread shall be on the thread list for that
thread's priority. Multiple scheduling policies shall be provided. Each non-empty thread list is ordered, contains a head as one
end of its order, and a tail as the other. The purpose of a scheduling policy is to define the allowable operations on this set of
lists (for example, moving threads between and within lists).

The POSIX model treats a "process" as an aggregation of system resources, including one or more threads that may
be scheduled by the operating system on the processor(s) it controls. Although a process has its own set of scheduling attributes,
these have an indirect effect (if any) on the scheduling behavior of individual threads as described below.

Each thread shall be controlled by an associated scheduling policy and priority. These parameters may be specified
by explicit application execution of the pthread_setschedparam()
function. Additionally, the scheduling parameters of a thread (but not its scheduling policy) may be changed by application
execution of the pthread_setschedprio() function.

Each process shall be controlled by an associated scheduling policy and priority. These parameters may be specified
by explicit application execution of the sched_setscheduler() or sched_setparam() functions.

The effect of the process scheduling attributes on individual threads in the process is dependent on the scheduling
contention scope of the threads (see 2.9.4 Thread Scheduling):

For threads with system scheduling contention scope, the process scheduling attributes shall have no effect on the
scheduling attributes or behavior either of the thread or an underlying kernel scheduling entity dedicated to that thread.

For threads with process scheduling contention scope, the process scheduling attributes shall have no effect on
the scheduling attributes of the thread. However, any underlying kernel scheduling entity used by these threads shall at all times
behave as specified by the scheduling attributes of the containing process, and this behavior may affect the scheduling behavior of
the process contention scope threads. For example, a process contention scope thread with scheduling policy SCHED_FIFO and the
system maximum priority H (the value returned by sched_get_priority_max(SCHED_FIFO)) in a process with scheduling
policy SCHED_RR and system minimum priority L (the value returned by sched_get_priority_min(SCHED_RR)) shall be
subject to timeslicing and to preemption by any thread with an effective priority higher than L.

Associated with each policy is a priority range. Each policy definition shall specify the minimum priority range
for that policy. The priority ranges for each policy may but need not overlap the priority ranges of other policies.

A conforming implementation shall select the thread that is defined as being at the head of the highest priority
non-empty thread list to become a running thread, regardless of its associated policy. This thread is then removed from its thread
list.

Four scheduling policies are specifically required. Other implementation-defined scheduling policies may be
defined. The following symbols are defined in the Base Definitions volume of POSIX.1-2024, <sched.h>:

SCHED_FIFO
First in, first out (FIFO) scheduling policy.
SCHED_RR
Round robin scheduling policy.
SCHED_SPORADIC
[SS]
Sporadic server scheduling policy.
SCHED_OTHER
Another scheduling policy.

The values of these symbols shall be distinct.

SCHED_FIFO

Conforming implementations shall include a scheduling policy called the FIFO scheduling policy.

Threads scheduled under this policy are chosen from a thread list that is ordered by the time its threads have been
on the list without being executed; generally, the head of the list is the thread that has been on the list the longest time, and
the tail is the thread that has been on the list the shortest time.

Under the SCHED_FIFO policy, the modification of the definitional thread lists is as follows:

When a running thread becomes a preempted thread, it becomes the head of the thread list for its priority.

When a blocked thread becomes a runnable thread, it becomes the tail of the thread list for its priority.

When a running thread calls the sched_setscheduler()
function, the process specified in the function call is modified to the specified policy and the priority specified by the
param argument.

When a running thread calls the sched_setparam() function,
the priority of the process specified in the function call is modified to the priority specified by the param argument.

When a running thread calls the pthread_setschedparam() function, the thread specified in the function call is
modified to the specified policy and the priority specified by the param argument.

When a running thread calls the pthread_setschedprio()
function, the thread specified in the function call is modified to the priority specified by the prio argument.

If a thread whose policy or priority has been modified other than by pthread_setschedprio() is a running thread or is runnable, it then becomes the
tail of the thread list for its new priority.

If a thread whose priority has been modified by pthread_setschedprio() is a running thread or is runnable, the effect on its
position in the thread list depends on the direction of the modification, as follows:

If the priority is raised, the thread becomes the tail of the thread list.

If the priority is unchanged, the thread does not change position in the thread list.

If the priority is lowered, the thread becomes the head of the thread list.

When a running thread issues the sched_yield() or thrd_yield() function, the thread becomes the tail of the thread list for its
priority.

At no other time is the position of a thread with this scheduling policy within the thread lists affected.

While a thread is executing at a temporarily elevated priority as a consequence of owning a mutex initialized with
the PTHREAD_PRIO_INHERIT or PTHREAD_PRIO_PROTECT protocol (see pthread_mutexattr_getprotocol()), the effects of the above
requirements on thread priority shall apply only to the thread's normal priority, not to its elevated priority, and those of the
above requirements that describe the thread being placed on any thread list as a result of a priority change shall not apply.
Likewise, when such a thread reverts to its normal priority as a consequence of unlocking such a mutex, those of the above
requirements that describe the thread being placed on any thread list as a result of a priority change shall not apply.

For this policy, valid priorities shall be within the range returned by the sched_get_priority_max() and sched_get_priority_min() functions when SCHED_FIFO is provided as the
parameter. Conforming implementations shall provide a priority range of at least 32 priorities for this policy.

SCHED_RR

Conforming implementations shall include a scheduling policy called the "round robin" scheduling policy. This
policy shall be identical to the SCHED_FIFO policy with the additional condition that when the implementation detects that a
running thread has been executing as a running thread for a time period of the length returned by the sched_rr_get_interval() function or longer, the thread shall become the tail
of its thread list and the head of that thread list shall be removed and made a running thread.

The effect of this policy is to ensure that if there are multiple SCHED_RR threads at the same priority, one of
them does not monopolize the processor. An application should not rely only on the use of SCHED_RR to ensure application progress
among multiple threads if the application includes threads using the SCHED_FIFO policy at the same or higher priority levels or
SCHED_RR threads at a higher priority level.

A thread under this policy that is preempted and subsequently resumes execution as a running thread completes the
unexpired portion of its round robin interval time period.

For this policy, valid priorities shall be within the range returned by the sched_get_priority_max() and sched_get_priority_min() functions when SCHED_RR is provided as the
parameter. Conforming implementations shall provide a priority range of at least 32 priorities for this policy.

SCHED_SPORADIC

[SS|TSP]  The functionality described in this section shall be provided on implementations that support the
Process Sporadic Server or Thread Sporadic Server options (and the rest of this section is not further marked for these options).

If _POSIX_SPORADIC_SERVER or _POSIX_THREAD_SPORADIC_SERVER is defined, the implementation shall include a
scheduling policy identified by the value SCHED_SPORADIC.

The sporadic server policy is based primarily on two time parameters: the replenishment period and the available
execution capacity. The replenishment period is given by the sched_ss_repl_period member of the sched_param
structure. The available execution capacity is initialized to the value given by the sched_ss_init_budget member of the same
parameter. The sporadic server policy is identical to the SCHED_FIFO policy with some additional conditions that cause the thread's
assigned priority to be switched between the values specified by the sched_priority and sched_ss_low_priority members
of the sched_param structure.

The priority assigned to a thread using the sporadic server scheduling policy is determined in the following
manner: if the available execution capacity is greater than zero and the number of pending replenishment operations is strictly
less than sched_ss_max_repl, the thread is assigned the priority specified by sched_priority; otherwise, the assigned
priority shall be sched_ss_low_priority. If the value of sched_priority is less than or equal to the value of
sched_ss_low_priority, the results are undefined. When active, the thread shall belong to the thread list corresponding to
its assigned priority level, according to the mentioned priority assignment. The modification of the available execution capacity
and, consequently of the assigned priority, is done as follows:

When the thread at the head of the sched_priority list becomes a running thread, its execution time shall
be limited to at most its available execution capacity, plus the resolution of the execution time clock used for this scheduling
policy. This resolution shall be implementation-defined.

Each time the thread is inserted at the tail of the list associated with sched_priority—because as a
blocked thread it became runnable with priority sched_priority or because a replenishment operation was performed—the time
at which this operation is done is posted as the activation_time.

When the running thread with assigned priority equal to sched_priority becomes a preempted thread, it
becomes the head of the thread list for its priority, and the execution time consumed is subtracted from the available execution
capacity. If the available execution capacity would become negative by this operation, it shall be set to zero.

When the running thread with assigned priority equal to sched_priority becomes a blocked thread, the
execution time consumed is subtracted from the available execution capacity, and a replenishment operation is scheduled, as
described in 6 and 7. If the available execution capacity would become negative by this operation, it shall be set to zero.

When the running thread with assigned priority equal to sched_priority reaches the limit imposed on its
execution time, it becomes the tail of the thread list for sched_ss_low_priority, the execution time consumed is subtracted
from the available execution capacity (which becomes zero), and a replenishment operation is scheduled, as described in 6 and
7.

Each time a replenishment operation is scheduled, the amount of execution capacity to be replenished,
replenish_amount, is set equal to the execution time consumed by the thread since the activation_time. The
replenishment is scheduled to occur at activation_time plus sched_ss_repl_period. If the scheduled time obtained is
before the current time, the replenishment operation is carried out immediately. Several replenishment operations can be pending at
the same time, each of which shall be serviced at its respective scheduled time. With the above rules, the number of replenishment
operations simultaneously pending for a given thread that is scheduled under the sporadic server policy shall not be greater than
sched_ss_max_repl.

A replenishment operation consists of adding the corresponding replenish_amount to the available execution
capacity at the scheduled time. If, as a consequence of this operation, the execution capacity would become larger than
sched_ss_initial_budget, it shall be rounded down to a value equal to sched_ss_initial_budget. Additionally, if the
thread was runnable or running, and had assigned priority equal to sched_ss_low_priority, then it becomes the tail of the
thread list for sched_priority.

Execution time is defined in XBD 3.90 CPU Time (Execution
Time).

For this policy, changing the value of a CPU-time clock via clock_settime() shall have no effect on its behavior.

For this policy, valid priorities shall be within the range returned by the sched_get_priority_min() and sched_get_priority_max() functions when SCHED_SPORADIC is provided as the
parameter. Conforming implementations shall provide a priority range of at least 32 distinct priorities for this policy.

If the scheduling policy of the target process is either SCHED_FIFO or SCHED_RR, the sched_ss_low_priority,
sched_ss_repl_period, and sched_ss_init budget members of the param argument shall have no effect on the
scheduling behavior. If the scheduling policy of this process is not SCHED_FIFO, SCHED_RR, or SCHED_SPORADIC, the effects of these
members are implementation-defined; this case includes the SCHED_OTHER policy.

SCHED_OTHER

Conforming implementations shall include one scheduling policy identified as SCHED_OTHER (which may execute
identically with either the FIFO or round robin scheduling policy). The effect of scheduling threads with the SCHED_OTHER policy in
a system in which other threads are executing under SCHED_FIFO, SCHED_RR, [SS]
or SCHED_SPORADIC  is implementation-defined.

This policy is defined to allow strictly conforming applications to be able to indicate in a portable manner that
they no longer need a realtime scheduling policy.

For threads executing under this policy, the implementation shall use only priorities within the range returned by
the sched_get_priority_max() and sched_get_priority_min() functions when SCHED_OTHER is provided as the
parameter.

2.8.5 Clocks and Timers

The <time.h> header defines the types and manifest constants
used by the timing facility.

Time Value Specification Structures

Many of the timing facility functions accept or return time value specifications. A time value structure
timespec specifies a single time value and includes at least the following members:

Member Type

Member Name

Description

time_t

tv_sec

Seconds.

long

tv_nsec

Nanoseconds.

The tv_nsec member is only valid if greater than or equal to zero, and less than the number of nanoseconds
in a second (1000 million). The time interval described by this structure is (tv_sec * 109 +
tv_nsec) nanoseconds.

A time value structure itimerspec specifies an initial timer value and a repetition interval for use by the
per-process timer functions. This structure includes at least the following members:

Member Type

Member Name

Description

struct timespec

it_interval

Timer period.

struct timespec

it_value

Timer expiration.

If the value described by it_value is non-zero, it indicates the time to or time of the next timer
expiration (for relative and absolute timer values, respectively). If the value described by it_value is zero, the timer
shall be disarmed.

If the value described by it_interval is non-zero, it specifies an interval which shall be used in reloading
the timer when it expires; that is, a periodic timer is specified. If the value described by it_interval is zero, the timer
is disarmed after its next expiration; that is, a one-shot timer is specified.

Timer Event Notification Control Block

Per-process timers may be created that notify the process of timer expirations by queuing a realtime extended
signal. The sigevent structure, defined in the Base Definitions volume of POSIX.1-2024, <signal.h>, is used in creating such a timer. The sigevent structure contains
the signal number and an application-specific data value which shall be used when notifying the calling process of timer expiration
events.

Manifest Constants

The following constants are defined in the Base Definitions volume of POSIX.1-2024, <time.h>:

CLOCK_REALTIME
The identifier for the system-wide realtime clock.
TIMER_ABSTIME
Flag indicating time is absolute with respect to the clock associated with a timer.
CLOCK_MONOTONIC
The identifier for the system-wide monotonic clock, which is defined as a clock whose value cannot be set via clock_settime() and which cannot have backward clock jumps. The maximum possible clock
jump is implementation-defined.

The maximum allowable resolution for CLOCK_REALTIME and CLOCK_MONOTONIC clocks and all time services based on these
clocks is represented by {_POSIX_CLOCKRES_MIN} and shall be defined as 20 ms (1/50 of a second). Implementations may support
smaller values of resolution for these clocks to provide finer granularity time bases. The actual resolution supported by an
implementation for a specific clock is obtained using the clock_getres()
function. If the actual resolution supported for a time service based on one of these clocks differs from the resolution supported
for that clock, the implementation shall document this difference.

The minimum allowable maximum value for CLOCK_REALTIME and CLOCK_MONOTONIC clocks and all absolute time services
based on them is the same as that defined by the ISO C standard for the time_t type. If the maximum value supported by
a time service based on one of these clocks differs from the maximum value supported by that clock, the implementation shall
document this difference.

Execution Time Monitoring

[CPT]  If _POSIX_CPUTIME is defined, process CPU-time clocks shall be supported in addition to the clocks described in
Manifest Constants.

[TCT]  If _POSIX_THREAD_CPUTIME is defined, thread CPU-time clocks shall be supported.

[CPT|TCT]  CPU-time clocks measure execution or CPU time, which is defined in XBD 3.90 CPU Time (Execution Time). The mechanism used to measure execution time is
described in XBD 4.14 Measurement of Execution Time.

[CPT]  If _POSIX_CPUTIME is defined, the following constant of the type clockid_t is defined in <time.h>:

CLOCK_PROCESS_CPUTIME_ID

When this value of the type clockid_t is used in a clock() or timer*()
function call, it is interpreted as the identifier of the CPU-time clock associated with the process making the function call.

[TCT]  If _POSIX_THREAD_CPUTIME is defined, the following constant of the type clockid_t is defined in <time.h>:

CLOCK_THREAD_CPUTIME_ID

When this value of the type clockid_t is used in a clock() or timer*()
function call, it is interpreted as the identifier of the CPU-time clock associated with the thread making the function call.

2.9 Threads

This section defines functionality to support multiple flows of control, called "threads", within a process. For
the definition of threads, see XBD 3.388 Thread.

The specific functional areas covered by threads and their scope include:

Thread management: the creation, control, and termination of multiple flows of control in the same process under
the assumption of a common shared address space

Synchronization primitives optimized for tightly coupled operation of multiple control flows in a common, shared
address space

2.9.1 Thread-Safety

All functions defined by this volume of POSIX.1-2024 shall be thread-safe, except that the following
functions1 need not be thread-safe.

asctime()

atomic_init()

catgets()

crypt()

ctime()

dbm_clearerr()

dbm_close()

dbm_delete()

dbm_error()

dbm_fetch()

dbm_firstkey()

dbm_nextkey()

dbm_open()

dbm_store()

dlerror()

drand48()

encrypt()

endgrent()

endpwent()

endutxent()

getdate()

getgrent()

getgrgid()

getgrnam()

gethostent()

getlogin()

getnetbyaddr()

getnetbyname()

getnetent()

getopt()

getprotobyname()

getprotobynumber()

getprotoent()

getpwent()

getpwnam()

getpwuid()

getservbyname()

getservbyport()

getservent()

getutxent()

getutxid()

getutxline()

gmtime()

hcreate()

hdestroy()

hsearch()

inet_ntoa()

l64a()

localeconv()

localtime()

lrand48()

mblen()

mbtowc()

mrand48()

nftw()

nl_langinfo()

ptsname()

putenv()

pututxline()

rand()

setenv()

setgrent()

setkey()

setlocale()

setpwent()

setutxent()

srand()

strerror()

strsignal()

strtok()

ttyname()

unsetenv()

wctomb()

The ctermid() and tmpnam() functions need not be thread-safe if passed a null pointer argument. The c16rtomb(), c32rtomb(), mbrlen(), mbrtoc16(), mbrtoc32(), mbrtowc(), mbsnrtowcs(), mbsrtowcs(), wcrtomb(), wcsnrtombs(), and wcsrtombs() functions need not be thread-safe if passed a null ps argument. The
lgamma(), lgammaf(), and lgammal() functions shall be thread-safe [XSI]  except that they
need not avoid data races when storing a value in the signgam variable.  The getc_unlocked(), getchar_unlocked(), putc_unlocked(), and putchar_unlocked() functions need not be thread-safe unless the invoking thread
owns the (FILE *) object accessed by the call, as is the case after a successful call to the flockfile() or ftrylockfile()
functions. The readdir() function need not be thread-safe if concurrent calls are
made for the same directory stream.

Some functions that are not required to be thread-safe are nevertheless required to avoid data races with either
all or some other functions, as specified on their individual reference pages.

Implementations shall provide internal synchronization as necessary in order to satisfy thread-safety
requirements.

Since multi-threaded applications are not allowed to use the environ variable to access or modify any
environment variable while any other thread is concurrently modifying any environment variable, the getenv() and secure_getenv() functions
and any function dependent on any environment variable are not thread-safe if another thread modifies the environment; see XSH
exec.

2.9.2 Thread IDs

Although implementations may have thread IDs that are unique in a system, applications should only assume that
thread IDs are usable and unique within a single process. The effect of calling any of the functions defined in this volume of
POSIX.1-2024 and passing as an argument the thread ID of a thread from another process is unspecified. The lifetime of a thread ID
ends after the later of thread termination (see 3.392 Thread Termination
) and the point when the thread is no longer joinable (see 3.183 Joinable
Thread). A conforming implementation is free to reuse a thread ID after its lifetime has ended. If an application attempts
to use a thread ID whose lifetime has ended, the behavior is undefined.

If a thread is detached, its thread ID is invalid for use as an argument in a call to pthread_detach(), pthread_join(),
thrd_detach(), or thrd_join().

2.9.3 Thread Mutexes

A thread that has blocked shall not prevent any unblocked thread that is eligible to use the same processing
resources from eventually making forward progress in its execution. Eligibility for processing resources is determined by the
scheduling policy.

A thread shall become the owner of a mutex, m, of type pthread_mutex_t when one of the following
occurs:

It calls pthread_mutex_clocklock(), pthread_mutex_lock(), pthread_mutex_timedlock(), or pthread_mutex_trylock() with m as the mutex argument and the
call returns zero or [EOWNERDEAD].

It calls pthread_mutex_setprioceiling() with
m as the mutex argument and the call returns [EOWNERDEAD].

It calls pthread_cond_clockwait(), pthread_cond_timedwait(), or pthread_cond_wait() with m as the mutex argument and the call
returns zero or certain error numbers (see pthread_cond_clockwait()
).

The thread shall remain the owner of m until one of the following occurs:

It executes pthread_mutex_unlock() with m as
the mutex argument

It blocks in a call to pthread_cond_clockwait(),
pthread_cond_timedwait(), or pthread_cond_wait() with m as the mutex argument.

A thread shall become the owner of a mutex, m, of type mtx_t when one of the following occurs:

It calls mtx_lock() with m as the mtx argument and
the call returns thrd_success.

It calls mtx_trylock() with m as the mtx argument
and the call returns thrd_success.

It calls mtx_timedlock() with m as the mtx
argument and the call returns thrd_success.

It calls cnd_wait() with m as the mtx argument and
the call returns thrd_success.

It calls cnd_timedwait() with m as the mtx
argument and the call returns thrd_success or thrd_timedout.

The thread shall remain the owner of m until one of the following occurs:

It executes mtx_unlock() with m as the mtx
argument.

It blocks in a call to cnd_wait() with m as the mtx
argument.

It blocks in a call to cnd_timedwait() with m as the
mtx argument.

The implementation shall behave as if at all times there is at most one owner of any mutex.

A thread that becomes the owner of a mutex is said to have "acquired" the mutex and the mutex is said to have
become "locked"; when a thread gives up ownership of a mutex it is said to have "released" the mutex and the mutex is said to
have become "unlocked".

A problem can occur if a process terminates while one of its threads holds a mutex lock. Depending on the mutex
type, it might be possible for another thread to unlock the mutex and recover the state of the mutex. However, it is difficult to
perform this recovery reliably.

Robust mutexes provide a means to enable the implementation to notify other threads in the event of a process
terminating while one of its threads holds a lock on a mutex of type pthread_mutex_t. The next thread that acquires the
mutex is notified about the termination by the return value [EOWNERDEAD] from the locking function. The notified thread can then
attempt to recover the state protected by the mutex, and if successful mark the state protected by the mutex as consistent by a
call to pthread_mutex_consistent(). If the notified thread is
unable to recover the state, it can declare the state as not recoverable by a call to pthread_mutex_unlock() without a prior call to pthread_mutex_consistent().

Whether or not the state protected by a mutex can be recovered is dependent solely on the application using robust
mutexes. The robust mutex support provided in the implementation provides notification only that a mutex owner has terminated while
holding a lock, or that the state of the mutex is not recoverable.

2.9.4 Thread Scheduling

[TPS]  The functionality described in this section shall be provided on implementations that support the Thread Execution
Scheduling option (and the rest of this section is not further marked for this option).

Thread Scheduling Attributes

In support of the scheduling function, threads have attributes which are accessed through the pthread_attr_t
thread creation attributes object.

The contentionscope attribute defines the scheduling contention scope of the thread to be either
PTHREAD_SCOPE_PROCESS or PTHREAD_SCOPE_SYSTEM.

The inheritsched attribute specifies whether a newly created thread is to inherit the scheduling attributes
of the creating thread or to have its scheduling values set according to the other scheduling attributes in the
pthread_attr_t object.

The schedpolicy attribute defines the scheduling policy for the thread. The schedparam attribute
defines the scheduling parameters for the thread. The interaction of threads having different policies within a process is
described as part of the definition of those policies.

If the Thread Execution Scheduling option is defined, and the schedpolicy attribute specifies one of the
priority-based policies defined under this option, the schedparam attribute contains the scheduling priority of the thread.
A conforming implementation ensures that the priority value in schedparam is in the range associated with the scheduling
policy when the thread attributes object is used to create a thread, or when the scheduling attributes of a thread are dynamically
modified. The meaning of the priority value in schedparam is the same as that of priority.

[TSP]  If _POSIX_THREAD_SPORADIC_SERVER is defined, the schedparam attribute supports four new members that are used
for the sporadic server scheduling policy. These members are sched_ss_low_priority, sched_ss_repl_period,
sched_ss_init_budget, and sched_ss_max_repl. The meaning of these attributes is the same as in the definitions that
appear under 2.8.4 Process Scheduling.

When a process is created, its single thread has a scheduling policy and associated attributes equal to the policy
and attributes of the process. The default scheduling contention scope value is implementation-defined. The default values of other
scheduling attributes are implementation-defined.

Thread Scheduling Contention Scope

The scheduling contention scope of a thread defines the set of threads with which the thread competes for use of
the processing resources. The scheduling operation selects at most one thread to execute on each processor at any point in time and
the thread's scheduling attributes (for example, priority), whether under process scheduling contention scope or system
scheduling contention scope, are the parameters used to determine the scheduling decision.

The scheduling contention scope, in the context of scheduling a mixed scope environment, affects threads as
follows:

A thread created with PTHREAD_SCOPE_SYSTEM scheduling contention scope contends for resources with all other
threads in the same scheduling allocation domain relative to their system scheduling attributes. The system scheduling attributes
of a thread created with PTHREAD_SCOPE_SYSTEM scheduling contention scope are the scheduling attributes with which the thread was
created. The system scheduling attributes of a thread created with PTHREAD_SCOPE_PROCESS scheduling contention scope are the
implementation-defined mapping into system attribute space of the scheduling attributes with which the thread was created.

Threads created with PTHREAD_SCOPE_PROCESS scheduling contention scope contend directly with other threads within
their process that were created with PTHREAD_SCOPE_PROCESS scheduling contention scope. The contention is resolved based on the
threads' scheduling attributes and policies. It is unspecified how such threads are scheduled relative to threads in other
processes or threads with PTHREAD_SCOPE_SYSTEM scheduling contention scope.

Conforming implementations shall support the PTHREAD_SCOPE_PROCESS scheduling contention scope, the
PTHREAD_SCOPE_SYSTEM scheduling contention scope, or both.

Scheduling Allocation Domain

Implementations shall support scheduling allocation domains containing one or more processors. It should be noted
that the presence of multiple processors does not automatically indicate a scheduling allocation domain size greater than one.
Conforming implementations on multi-processors may map all or any subset of the CPUs to one or multiple scheduling allocation
domains, and could define these scheduling allocation domains on a per-thread, per-process, or per-system basis, depending on the
types of applications intended to be supported by the implementation. The scheduling allocation domain is independent of scheduling
contention scope, as the scheduling contention scope merely defines the set of threads with which a thread contends for processor
resources, while scheduling allocation domain defines the set of processors for which it contends. The semantics of how this
contention is resolved among threads for processors is determined by the scheduling policies of the threads.

The choice of scheduling allocation domain size and the level of application control over scheduling allocation
domains is implementation-defined. Conforming implementations may change the size of scheduling allocation domains and the binding
of threads to scheduling allocation domains at any time.

For application threads with scheduling allocation domains of size equal to one, the scheduling rules defined for
SCHED_FIFO and SCHED_RR shall be used; see Scheduling Policies. All threads with system scheduling
contention scope, regardless of the processes in which they reside, compete for the processor according to their priorities.
Threads with process scheduling contention scope compete only with other threads with process scheduling contention scope within
their process.

For application threads with scheduling allocation domains of size greater than one, the rules defined for
SCHED_FIFO, SCHED_RR, [TSP]   and SCHED_SPORADIC  shall be used
in an implementation-defined manner. Each thread with system scheduling contention scope competes for the processors in its
scheduling allocation domain in an implementation-defined manner according to its priority. Threads with process scheduling
contention scope are scheduled relative to other threads within the same scheduling contention scope in the process.

[TSP]  If _POSIX_THREAD_SPORADIC_SERVER is defined, the rules defined for SCHED_SPORADIC in Scheduling Policies shall be used in an implementation-defined manner for application threads whose
scheduling allocation domain size is greater than one.

Scheduling Documentation

If _POSIX_PRIORITY_SCHEDULING is defined, then any scheduling policies beyond SCHED_OTHER, SCHED_FIFO, SCHED_RR,
[TSP]
and SCHED_SPORADIC,  as well as the effects of the scheduling
policies indicated by these other values, and the attributes required in order to support such a policy, are
implementation-defined. Furthermore, the implementation shall document the effect of all processor scheduling allocation domain
values supported for these policies.

2.9.5 Thread Cancellation

The thread cancellation mechanism allows a thread to terminate the execution of any other thread in the process,
except for threads created using thrd_create(), in a controlled manner. The
target thread (that is, the one that is being canceled) is allowed to hold cancellation requests pending in a number of ways and to
perform application-specific cleanup processing when the notice of cancellation is acted upon.

Cancellation is controlled by the cancellation control functions. Each thread maintains its own cancelability
state. Cancellation may only occur at cancellation points or when the thread is asynchronously cancelable.

The thread cancellation mechanism described in this section depends upon programs having set deferred
cancelability state, which is specified as the default. Applications shall also carefully follow static lexical scoping rules in
their execution behavior. For example, use of setjmp(), return, goto,
and so on, to leave user-defined cancellation scopes without doing the necessary scope pop operation results in undefined
behavior.

Use of asynchronous cancelability while holding resources which potentially need to be released may result in
resource loss. Similarly, cancellation scopes may only be safely manipulated (pushed and popped) when the thread is in the
deferred or disabled cancelability states.

2.9.5.1 Cancelability States

The cancelability state of a thread determines the action taken upon receipt of a cancellation request. The thread
may control cancellation in a number of ways.

Each thread maintains its own cancelability state, which may be encoded in two bits:

Cancelability-Enable: When cancelability is PTHREAD_CANCEL_DISABLE (as defined in the Base Definitions volume of
POSIX.1-2024, <pthread.h>), cancellation requests against the target thread
are held pending. By default, cancelability is set to PTHREAD_CANCEL_ENABLE (as defined in <pthread.h>).

Cancelability Type: When cancelability is enabled and the cancelability type is PTHREAD_CANCEL_ASYNCHRONOUS (as
defined in <pthread.h>), new or pending cancellation requests may be acted
upon at any time. When cancelability is enabled and the cancelability type is PTHREAD_CANCEL_DEFERRED (as defined in <pthread.h>), cancellation requests are held pending until a cancellation point (see
below) is reached. If cancelability is disabled, the setting of the cancelability type has no immediate effect as all cancellation
requests are held pending; however, once cancelability is enabled again the new type is in effect. The cancelability type is
PTHREAD_CANCEL_DEFERRED in all newly created threads including the thread in which main() was first invoked.

2.9.5.2 Cancellation Points

Cancellation points shall occur when a thread is executing the following functions:

accept()

accept4()

aio_suspend()

clock_nanosleep()

close()

cnd_timedwait()

cnd_wait()

connect()

creat()

fcntl()†

fdatasync()

fsync()

lockf()††

mq_receive()

mq_send()

mq_timedreceive()

mq_timedsend()

msgrcv()

msgsnd()

msync()

nanosleep()

open()

openat()

pause()

poll()

posix_close()

ppoll()

pread()

pselect()

pthread_cond_clockwait()

pthread_cond_timedwait()

pthread_cond_wait()

pthread_join()

pthread_testcancel()

pwrite()

read()

readv()

recv()

recvfrom()

recvmsg()

select()

send()

sendmsg()

sendto()

sigsuspend()

sigtimedwait()

sigwait()

sigwaitinfo()

sleep()

tcdrain()

thrd_join()

thrd_sleep()

wait()

waitid()

waitpid()

write()

writev()

A cancellation point may also occur when a thread is executing the following functions:

access()

bindtextdomain()

catclose()

catopen()

chmod()

chown()

closedir()

closelog()

ctermid()

dcgettext()

dcgettext_l()

dcngettext()

dcngettext_l()

dgettext()

dgettext_l()

dlclose()

dlopen()

dngettext()

dngettext_l()

dprintf()

endhostent()

endnetent()

endprotoent()

endservent()

faccessat()

fchmod()

fchmodat()

fchown()

fchownat()

fclose()

fcntl()†††

fflush()

fgetc()

fgetpos()

fgets()

fgetwc()

fgetws()

fmtmsg()

fopen()

fpathconf()

fprintf()

fputc()

fputs()

fputwc()

fputws()

fread()

freopen()

fscanf()

fseek()

fseeko()

fsetpos()

fstat()

fstatat()

ftell()

ftello()

futimens()

fwprintf()

fwrite()

fwscanf()

getaddrinfo()

getc()

getc_unlocked()

getchar()

getchar_unlocked()

getcwd()

getdelim()

getgrgid_r()

getgrnam_r()

gethostid()

gethostname()

getline()

getlogin_r()

getnameinfo()

getpwnam_r()

getpwuid_r()

gettext()

gettext_l()

getwc()

getwchar()

glob()

iconv_close()

iconv_open()

link()

linkat()

lio_listio()

localtime_r()

lockf()

lseek()

lstat()

mkdir()

mkdirat()

mkdtemp()

mkfifo()

mkfifoat()

mknod()

mknodat()

mkstemp()

mktime()

ngettext()

ngettext_l()

opendir()

openlog()

pathconf()

perror()

popen()

posix_devctl()

posix_fadvise()

posix_fallocate()

posix_getdents()

posix_madvise()

posix_openpt()

posix_spawn()

posix_spawnp()

posix_typed_mem_open()

printf()

psiginfo()

psignal()

pthread_rwlock_clockrdlock()

pthread_rwlock_clockwrlock()

pthread_rwlock_rdlock()

pthread_rwlock_timedrdlock()

pthread_rwlock_timedwrlock()

pthread_rwlock_wrlock()

ptsname()

ptsname_r()

putc()

putc_unlocked()

putchar()

putchar_unlocked()

puts()

putwc()

putwchar()

readdir_r()

readlink()

readlinkat()

remove()

rename()

renameat()

rewind()

rewinddir()

scandir()

scanf()

seekdir()

sem_clockwait()

sem_timedwait()

sem_wait()

semop()

sethostent()

setnetent()

setprotoent()

setservent()

stat()

strerror_l()

strerror_r()

strftime()

strftime_l()

symlink()

symlinkat()

sync()

syslog()

tmpfile()

tmpnam()

ttyname_r()

tzset()

ungetc()

ungetwc()

unlink()

unlinkat()

utimensat()

utimes()

vdprintf()

vfprintf()

vfwprintf()

vprintf()

vwprintf()

wcsftime()

wordexp()

wprintf()

wscanf()

In addition, a cancellation point may occur when a thread is executing any function that this standard does not
require to be thread-safe but the implementation documents as being thread-safe. If a thread is cancelled while executing a
non-thread-safe function, the behavior is undefined.

An implementation shall not introduce cancellation points into any other functions specified in this volume of
POSIX.1-2024.

The side-effects of acting upon a cancellation request while suspended during a call of a function are the same as
the side-effects that may be seen in a single-threaded program when a call to a function is interrupted by a signal and the given
function returns [EINTR]. Any such side-effects occur before any cancellation cleanup handlers are called. For functions that are
explicitly required not to return when interrupted (for example, pclose()), if a
thread is canceled while executing the function, the behavior is undefined.

Whenever a thread has cancelability enabled and a cancellation request has been made with that thread as the
target, and the thread then calls any function that is a cancellation point (such as pthread_testcancel() or read()), the
cancellation request shall be acted upon before the function returns. If a thread has cancelability enabled and a cancellation
request is made with the thread as a target while the thread is suspended at a cancellation point, the thread shall be awakened and
the cancellation request shall be acted upon. It is unspecified whether the cancellation request is acted upon or whether the
cancellation request remains pending and the thread resumes normal execution if the thread is suspended at a cancellation point and
either:

The event for which it is waiting occurs

A specified timeout expires

before the cancellation request is acted upon.

2.9.5.3 Thread Cancellation Cleanup Handlers

Each thread that was not created using thrd_create() maintains a
list of cancellation cleanup handlers. The programmer uses the pthread_cleanup_push() and pthread_cleanup_pop() functions to place routines on and remove routines from
this list.

When a cancellation request is acted upon, or when a thread calls pthread_exit(), the thread first disables cancellation by setting its cancelability
state to PTHREAD_CANCEL_DISABLE and its cancelability type to PTHREAD_CANCEL_DEFERRED. The cancelability state shall remain set to
PTHREAD_CANCEL_DISABLE until the thread has terminated. The behavior is undefined if a cancellation cleanup handler or
thread-specific data destructor routine changes the cancelability state to PTHREAD_CANCEL_ENABLE.

The routines in the thread's list of cancellation cleanup handlers shall be invoked one by one in LIFO sequence;
that is, the last routine pushed onto the list (Last In) is the first to be invoked (First Out). When the cancellation cleanup
handler for a scope is invoked, the storage for that scope remains valid. If the last cancellation cleanup handler returns,
thread-specific data destructors (if any) associated with thread-specific data keys for which the thread has non-NULL values shall
be run, in unspecified order, as described for pthread_key_create() and
tss_create().

After all cancellation cleanup handlers and thread-specific data destructors have returned, thread execution is
terminated. If the thread has terminated because of a call to pthread_exit(),
the value_ptr argument is made available to any threads joining with the target. If the thread has terminated by acting on a
cancellation request, a status of PTHREAD_CANCELED is made available to any threads joining with the target. The symbolic constant
PTHREAD_CANCELED expands to a constant expression of type (void *) whose value matches no pointer to an object in memory nor
the value NULL.

A side-effect of acting upon a cancellation request while in a condition variable wait is that the mutex is
re-acquired before calling the first cancellation cleanup handler. In addition, the thread is no longer considered to be waiting
for the condition and the thread shall not have consumed any pending condition signals on the condition.

A cancellation cleanup handler cannot exit via longjmp() or siglongjmp().

2.9.5.4 Async-Cancel Safety

The pthread_cancel(), pthread_setcancelstate(), and pthread_setcanceltype() functions are defined to be async-cancel safe.

No other functions in this volume of POSIX.1-2024 are required to be async-cancel-safe.

If a thread has asynchronous cancellation enabled and is cancelled during execution of a function that is not
async-cancel-safe, the behavior is undefined.

If a thread has deferred cancellation enabled, a signal-catching function is called in that thread during execution
of a function that is not async-cancel-safe, and the signal-catching function calls any function that is a cancellation point while
a cancellation is pending for the thread, without first disabling cancellation, the behavior is undefined.

2.9.6 Thread Read-Write Locks

Multiple readers, single writer (read-write) locks allow many threads to have simultaneous read-only access to data
while allowing only one thread to have exclusive write access at any given time. They are typically used to protect data that is
read more frequently than it is changed.

One or more readers acquire read access to the resource by performing a read lock operation on the associated
read-write lock. A writer acquires exclusive write access by performing a write lock operation. Basically, all readers exclude any
writers and a writer excludes all readers and any other writers.

A thread that has blocked on a read-write lock (for example, has not yet returned from a pthread_rwlock_rdlock() or pthread_rwlock_wrlock() call) shall not prevent any unblocked thread that is
eligible to use the same processing resources from eventually making forward progress in its execution. Eligibility for processing
resources shall be determined by the scheduling policy.

Read-write locks can be used to synchronize threads in the current process and other processes if they are
allocated in memory that is writable and shared among the cooperating processes and have been initialized for this behavior.

2.9.7 Thread Interactions with File Operations

All of the following functions shall be atomic with respect to each other in the effects specified in POSIX.1-2024
when they operate on files in the file hierarchy:

chmod()

chown()

creat()

fchmod()

fchmodat()

fchown()

fchownat()

fstat()

fstatat()

ftruncate()

futimens()

lchown()

link()

linkat()

lstat()

open()

openat()

readlink()

readlinkat()

rename()

renameat()

stat()

symlink()

symlinkat()

truncate()

unlink()

unlinkat()

utimensat()

utimes()

If two threads each call one of these functions, each call shall either see all of the specified effects of the
other call, or none of them.

Except where specified otherwise, all of the following functions shall be atomic with respect to each other in the
effects specified in POSIX.1-2024 when they operate on file descriptors that are open, or being opened, to files in the file
hierarchy:

close()

dup2()

dup3()

fcntl()

fstat()

fstatat()

ftruncate()

futimens()

lseek()

open()

openat()

pread()

read()

readv()

pwrite()

write()

writev()

If two threads each call one of these functions, each call shall either see all of the specified effects of the
other call, or none of them. The requirement on the close() function shall also apply
whenever a file descriptor is successfully closed, however caused (for example, as a consequence of calling close(), calling dup2(), or of process
termination).

2.9.8 Use of Application-Managed Thread Stacks

An "application-managed thread stack" is a region of memory allocated by the application—for example, memory
returned by the malloc() or mmap()
functions—and designated as a stack through the act of passing the address and size of the stack, respectively, as the
stackaddr and stacksize arguments to pthread_attr_setstack(). Application-managed stacks allow the application to
precisely control the placement and size of a stack.

The application grants to the implementation permanent ownership of and control over the application-managed stack
when the attributes object in which the stack or stackaddr attribute has been set is used, either by presenting that
attribute's object as the attr argument in a call to pthread_create()
that completes successfully, or by storing a pointer to the attributes object in the sigev_notify_attributes member of a
struct sigevent and passing that struct sigevent to a function accepting such argument that completes successfully.
The application may thereafter utilize the memory within the stack only within the normal context of stack usage within or properly
synchronized with a thread that has been scheduled by the implementation with stack pointer value(s) that are within the range of
that stack. In particular, the region of memory cannot be freed, nor can it be later specified as the stack for another thread.

When specifying an attributes object with an application-managed stack through the sigev_notify_attributes
member of a struct sigevent, the results are undefined if the requested signal is generated multiple times (as for a
repeating timer).

Until an attributes object in which the stack or stackaddr attribute has been set is used, the
application retains ownership of and control over the memory allocated to the stack. It may free or reuse the memory as long as it
either deletes the attributes object, or before using the attributes object replaces the stack by making an additional call to
pthread_attr_setstack(), that was used originally to designate the
stack. There is no mechanism to retract the reference to an application-managed stack by an existing attributes object.

Once an attributes object with an application-managed stack has been used, that attributes object cannot be used
again by a subsequent call to pthread_create() or any function accepting a
struct sigevent with sigev_notify_attributes containing a pointer to the attributes object, without designating an
unused application-managed stack by making an additional call to pthread_attr_setstack().

2.9.9 Synchronization Object Copies and Alternative Mappings

For barriers, condition variables, mutexes, and read-write locks, [TSH]   if the
process-shared attribute is set to PTHREAD_PROCESS_PRIVATE,
only the synchronization object at the address used to initialize it can be used for performing synchronization. The effect
of referring to another mapping of the same object when locking, unlocking, or destroying the object is undefined. [TSH]   If the
process-shared attribute is set to PTHREAD_PROCESS_SHARED, only the synchronization object itself can be used for performing
synchronization; however, it need not be referenced at the address used to initalize it (that is, another mapping of the same
object can be used).   The effect of referring to a copy of the
object when locking, unlocking, or destroying it is undefined.

For spin locks, the above requirements shall apply as if spin locks have a process-shared attribute that is set
from the pshared argument to pthread_spin_init(). For semaphores,
the above requirements shall apply as if semaphores have a process-shared attribute that is set to PTHREAD_PROCESS_PRIVATE if the
pshared argument to sem_init() is zero and set to PTHREAD_PROCESS_SHARED if
pshared is non-zero.

For ISO C functions declared in <threads.h>, the above
requirements shall apply as if condition variables of type cnd_t and mutexes of type mtx_t have a process-shared
attribute that is set to PTHREAD_PROCESS_PRIVATE.

2.10 Sockets

A socket is an endpoint for communication using the facilities described in this section. A socket is created with
a specific socket type, described in 2.10.6 Socket Types, and is associated with a specific protocol,
detailed in 2.10.3 Protocols. A socket is accessed via a file descriptor obtained when the socket is
created.

2.10.1 Address Families

All network protocols are associated with a specific address family. An address family provides basic services to
the protocol implementation to allow it to function within a specific network environment. These services may include packet
fragmentation and reassembly, routing, addressing, and basic transport. An address family is normally comprised of a number of
protocols, one per socket type. Each protocol is characterized by an abstract socket type. It is not required that an address
family support all socket types. An address family may contain multiple protocols supporting the same socket abstraction.

2.10.17 Use of Sockets for Local UNIX Connections, 2.10.19 Use
of Sockets over Internet Protocols Based on IPv4, and 2.10.20 Use of Sockets over Internet Protocols
Based on IPv6, respectively, describe the use of sockets for local UNIX connections, for Internet protocols based on IPv4, and
for Internet protocols based on IPv6.

2.10.2 Addressing

An address family defines the format of a socket address. All network addresses are described using a general
structure, called a sockaddr, as defined in the Base Definitions volume of POSIX.1-2024, <sys/socket.h>. However, each address family imposes finer and more specific
structure, generally defining a structure with fields specific to the address family. The field sa_family in the
sockaddr structure contains the address family identifier, specifying the format of the sa_data area. The size of the
sa_data area is unspecified.

2.10.3 Protocols

A protocol supports one of the socket abstractions detailed in 2.10.6 Socket Types.
Selecting a protocol involves specifying the address family, socket type, and protocol number to the socket() function. Certain semantics of the basic socket abstractions are protocol-specific.
All protocols are expected to support the basic model for their particular socket type, but may, in addition, provide non-standard
facilities or extensions to a mechanism.

2.10.4 Routing

Sockets provides packet routing facilities. A routing information database is maintained, which is used in
selecting the appropriate network interface when transmitting packets.

2.10.5 Interfaces

Each network interface in a system corresponds to a path through which messages can be sent and received. A network
interface usually has a hardware device associated with it, though certain interfaces such as the loopback interface, do not.

2.10.6 Socket Types

A socket is created with a specific type, which defines the communication semantics and which allows the selection
of an appropriate communication protocol. Four types are defined: SOCK_DGRAM, [RS]   SOCK_RAW,
SOCK_SEQPACKET, and SOCK_STREAM. Implementations may specify
additional socket types.

The SOCK_STREAM socket type provides reliable, sequenced, full-duplex octet streams between the socket and a peer
to which the socket is connected. A socket of type SOCK_STREAM needs to be in a connected state before any data can be sent or
received. Record boundaries are not maintained; data sent on a stream socket using output operations of one size can be received
using input operations of smaller or larger sizes without loss of data. Data may be buffered; successful return from an output
function does not imply that the data has been delivered to the peer or even transmitted from the local system. If data cannot be
successfully transmitted within a given time then the connection is considered broken, and subsequent operations shall fail. A
SIGPIPE signal is raised if a thread attempts to send data on a broken stream (one that is no longer connected), except that the
signal is suppressed if the MSG_NOSIGNAL flag is used in calls to send(), sendto(), and sendmsg(). Support for an
out-of-band data transmission facility is protocol-specific.

The SOCK_SEQPACKET socket type is similar to the SOCK_STREAM type, and is also connection-oriented. The only
difference between these types is that record boundaries are maintained using the SOCK_SEQPACKET type. A record can be sent using
one or more output operations and received using one or more input operations, but a single operation never transfers parts of more
than one record. Record boundaries are visible to the receiver via the MSG_EOR flag in the received message flags returned by the
recvmsg() function. It is protocol-specific whether a maximum record size is
imposed.

The SOCK_DGRAM socket type supports connectionless data transfer which is not necessarily acknowledged or reliable.
Datagrams can be sent to the address specified (possibly multicast or broadcast) in each output operation, and incoming datagrams
can be received from multiple sources. The source address of each datagram is available when receiving the datagram. An application
can also pre-specify a peer address, in which case calls to output functions that do not specify a peer address shall send to the
pre-specified peer. If a peer has been specified, only datagrams from that peer shall be received. A datagram shall be sent in a
single output operation, and needs to be received in a single input operation. The maximum size of a datagram is protocol-specific;
with some protocols, the limit is implementation-defined. Output datagrams may be buffered within the system; thus, a successful
return from an output function does not guarantee that a datagram is actually sent or received. However, implementations should
attempt to detect any errors possible before the return of an output function, reporting any error by an unsuccessful return
value.

[RS]  The SOCK_RAW socket type is similar to the SOCK_DGRAM type. It differs in that it is normally used with communication
providers that underlie those used for the other socket types. For this reason, the creation of a socket with type SOCK_RAW shall
require appropriate privileges. The format of datagrams sent and received with this socket type generally include specific protocol
headers, and the formats are protocol-specific and implementation-defined.

2.10.7 Socket I/O Mode

The I/O mode of a socket is described by the O_NONBLOCK file status flag which pertains to the open file
description for the socket. This flag is initially off when a socket is created, but may be set and cleared by the use of the
F_SETFL command of the fcntl() function.

When the O_NONBLOCK flag is set, certain functions that would normally block until they are complete shall return
immediately.

The bind() function initiates an address assignment and shall return
without blocking when O_NONBLOCK is set; if the socket address cannot be assigned immediately, bind() shall return the [EINPROGRESS] error to indicate that the assignment was initiated
successfully, but that it has not yet completed.

The connect() function initiates a connection and shall return
without blocking when O_NONBLOCK is set; it shall return the error [EINPROGRESS] to indicate that the connection was initiated
successfully, but that it has not yet completed.

Data transfer operations (the read(), write(), send(), and recv() functions) shall complete immediately, transfer only as much as is available, and then
return without blocking, or return an error indicating that no transfer could be made without blocking.

2.10.8 Socket Owner

The owner of a socket is unset when a socket is created. The owner may be set to a process ID or process group ID
using the F_SETOWN command of the fcntl() function.

2.10.9 Socket Queue Limits

The transmit and receive queue sizes for a socket are set when the socket is created. The default sizes used are
both protocol-specific and implementation-defined. The sizes may be changed using the setsockopt() function.

2.10.10 Pending Error

Errors may occur asynchronously, and be reported to the socket in response to input from the network protocol. The
socket stores the pending error to be reported to a user of the socket at the next opportunity. The error is returned in response
to a subsequent send(), recv(), or getsockopt() operation on the socket, and the pending error is then cleared.

2.10.11 Socket Receive Queue

A socket has a receive queue that buffers data when it is received by the system until it is removed by a receive
call. Depending on the type of the socket and the communication provider, the receive queue may also contain ancillary data such as
the addressing and other protocol data associated with the normal data in the queue, and may contain out-of-band or expedited data.
The limit on the queue size includes any normal, out-of-band data, datagram source addresses, and ancillary data in the queue. The
description in this section applies to all sockets, even though some elements cannot be present in some instances.

The contents of a receive buffer are logically structured as a series of data segments with associated ancillary
data and other information. A data segment may contain normal data or out-of-band data, but never both. A data segment may complete
a record if the protocol supports records (always true for types SOCK_SEQPACKET and SOCK_DGRAM). A record may be stored as more
than one segment; the complete record might never be present in the receive buffer at one time, as a portion might already have
been returned to the application, and another portion might not yet have been received from the communications provider. A data
segment may contain ancillary protocol data, which is logically associated with the segment. Ancillary data is received as if it
were queued along with the first normal data octet in the segment (if any). A segment may contain ancillary data only, with no
normal or out-of-band data. For the purposes of this section, a datagram is considered to be a data segment that terminates a
record, and that includes a source address as a special type of ancillary data. Data segments are placed into the queue as data is
delivered to the socket by the protocol. Normal data segments are placed at the end of the queue as they are delivered. If a new
segment contains the same type of data as the preceding segment and includes no ancillary data, and if the preceding segment does
not terminate a record, the segments are logically merged into a single segment.

The receive queue is logically terminated if an end-of-file indication has been received or a connection has been
terminated. A segment shall be considered to be terminated if another segment follows it in the queue, if the segment completes a
record, or if an end-of-file or other connection termination has been reported. The last segment in the receive queue shall also be
considered to be terminated while the socket has a pending error to be reported.

A receive operation shall never return data or ancillary data from more than one segment.

2.10.12 Socket Out-of-Band Data State

The handling of received out-of-band data is protocol-specific. Out-of-band data may be placed in the socket
receive queue, either at the end of the queue or before all normal data in the queue. In this case, out-of-band data is returned to
an application program by a normal receive call. Out-of-band data may also be queued separately rather than being placed in the
socket receive queue, in which case it shall be returned only in response to a receive call that requests out-of-band data. It is
protocol-specific whether an out-of-band data mark is placed in the receive queue to demarcate data preceding the out-of-band data
and following the out-of-band data. An out-of-band data mark is logically an empty data segment that cannot be merged with other
segments in the queue. An out-of-band data mark is never returned in response to an input operation. The sockatmark() function can be used to test whether an out-of-band data mark is the first
element in the queue. If an out-of-band data mark is the first element in the queue when an input function is called without the
MSG_PEEK option, the mark is removed from the queue and the following data (if any) is processed as if the mark had not been
present.

2.10.13 Connection Indication Queue

Sockets that are used to accept incoming connections maintain a queue of outstanding connection indications. This
queue is a list of connections that are awaiting acceptance by the application; see listen().

2.10.14 Signals

One category of event at the socket interface is the generation of signals. These signals report protocol events or
process errors relating to the state of the socket. The generation or delivery of a signal does not change the state of the socket,
although the generation of the signal may have been caused by a state change.

The SIGPIPE signal shall be sent to a thread that attempts to send data on a socket that is no longer able to send
(one that is no longer connected), except that the signal is suppressed if the MSG_NOSIGNAL flag is used in calls to send(), sendto(), and sendmsg(). Regardless of whether the generation of the signal is suppressed, the send
operation shall fail with the [EPIPE] error.

If a socket has an owner, the SIGURG signal is sent to the owner of the socket when it is notified of expedited or
out-of-band data. The socket state at this time is protocol-dependent, and the status of the socket is specified in 2.10.17 Use of Sockets for Local UNIX Connections, 2.10.19 Use of Sockets over
Internet Protocols Based on IPv4, and 2.10.20 Use of Sockets over Internet Protocols Based on IPv6
. Depending on the protocol, the expedited data may or may not have arrived at the time of signal generation.

2.10.15 Asynchronous Errors

If any of the following conditions occur asynchronously for a socket, the corresponding value listed below shall
become the pending error for the socket:

[ECONNABORTED]

The connection was aborted locally.
[ECONNREFUSED]

For a connection-mode socket attempting a non-blocking connection, the attempt to connect was forcefully rejected. For a
connectionless-mode socket, an attempt to deliver a datagram was forcefully rejected.
[ECONNRESET]

The peer has aborted the connection.
[EHOSTUNREACH]

The destination host is not reachable.
[EMSGSIZE]

For a connectionless-mode socket, the size of a previously sent datagram prevented delivery.
[ENETDOWN]

The local network connection is not operational.
[ENETRESET]

The connection was aborted by the network.
[ENETUNREACH]

The destination network is not reachable.

2.10.16 Use of Options

There are a number of socket options which either specialize the behavior of a socket or provide useful
information. These options may be set at different protocol levels and are always present at the uppermost "socket" level.

Socket options are manipulated by two functions, getsockopt() and
setsockopt(). These functions allow an application program to customize the
behavior and characteristics of a socket to provide the desired effect.

All of the options usable with setsockopt() have defaults. For
each option where a default value is listed as implementation-defined, the implementation also controls whether a socket created by
accept() or accept4() starts with the
option reset to the original default value, or inherited as the value previously customized on the original listening socket. The
type and meaning of these values is defined by the protocol level to which they apply. Instead of using the default values, an
application program may choose to customize one or more of the options. However, in the bulk of cases, the default values are
sufficient for the application.

Some of the options are used to enable or disable certain behavior within the protocol modules (for example, turn
on debugging) while others may be used to set protocol-specific information (for example, IP time-to-live on all the application's
outgoing packets). As each of the options is introduced, its effect on the underlying protocol modules is described.

Value of Level for Socket Options shows the value for the socket level.

Table: Value of Level for Socket Options

Name

Description

SOL_SOCKET

Options are intended for the sockets level.

Socket-Level Options lists those options present at the socket level; that is, when the
level parameter of the getsockopt() or setsockopt() function is SOL_SOCKET, the types of the option value parameters associated
with each option, and a brief synopsis of the meaning of the option value parameter. Unless otherwise noted, each may be examined
with getsockopt() and set with setsockopt() on all types of socket. Options at other protocol levels vary in format and
name.

Table: Socket-Level Options

Option

Parameter Type

Parameter Meaning

SO_ACCEPTCONN

int

Non-zero indicates that socket listening is enabled (getsockopt()
only).

SO_BROADCAST

int

Non-zero requests permission to transmit broadcast datagrams (SOCK_DGRAM sockets only).

SO_DEBUG

int

Non-zero requests debugging in underlying protocol modules.

SO_DOMAIN

int

Identify socket domain (getsockopt() only).

SO_DONTROUTE

int

Non-zero requests bypass of normal routing; route based on destination address only.

SO_ERROR

int

Requests and clears pending error information on the socket (getsockopt() only).

SO_KEEPALIVE

int

Non-zero requests periodic transmission of keepalive messages (protocol-specific).

SO_LINGER

struct linger

Specify actions to be taken for queued, unsent data on close(): linger
on/off and linger time in seconds.

SO_OOBINLINE

int

Non-zero requests that out-of-band data be placed into normal data input queue as received.

SO_PROTOCOL

int

Identify socket protocol (getsockopt() only).

SO_RCVBUF

int

Size of receive buffer (in bytes).

SO_RCVLOWAT

int

Minimum amount of data to return to application for input operations (in bytes).

SO_RCVTIMEO

struct timeval

Timeout value for a socket receive operation.

SO_REUSEADDR

int

Non-zero requests reuse of local addresses in bind()
(protocol-specific).

SO_SNDBUF

int

Size of send buffer (in bytes).

SO_SNDLOWAT

int

Minimum amount of data to send for output operations (in bytes).

SO_SNDTIMEO

struct timeval

Timeout value for a socket send operation.

SO_TYPE

int

Identify socket type (getsockopt() only).

The SO_ACCEPTCONN option is used only on getsockopt(). When this
option is specified, getsockopt() shall report whether socket listening is
enabled for the socket. A value of zero shall indicate that socket listening is disabled; non-zero that it is enabled.
SO_ACCEPTCONN has no default value.

The SO_BROADCAST option requests permission to send broadcast datagrams on the socket. Support for SO_BROADCAST is
protocol-specific. The default for SO_BROADCAST is that the ability to send broadcast datagrams on a socket is disabled.

The SO_DEBUG option enables debugging in the underlying protocol modules. This can be useful for tracing the
behavior of the underlying protocol modules during normal system operation. The semantics of the debug reports are
implementation-defined. The default value for SO_DEBUG is for debugging to be turned off.

The SO_DOMAIN option is used only on getsockopt(). When this
option is specified, getsockopt() shall return the domain of the socket (for
example, AF_INET6). SO_DOMAIN has no default value.

The SO_DONTROUTE option requests that outgoing messages bypass the standard routing facilities. The destination
needs to be on a directly-connected network, and messages are directed to the appropriate network interface according to the
destination address. It is protocol-specific whether this option has any effect and how the outgoing network interface is chosen.
Support for this option with each protocol is implementation-defined.

The SO_ERROR option is used only on getsockopt(). When this
option is specified, getsockopt() shall return any pending error on the socket
and clear the error status. It shall return a value of 0 if there is no pending error. SO_ERROR may be used to check for
asynchronous errors on connected connectionless-mode sockets or for other types of asynchronous errors. SO_ERROR has no default
value.

The SO_KEEPALIVE option enables the periodic transmission of messages on a connected socket. The behavior of this
option is protocol-specific. On a connection-mode socket for which a connection has been established, if SO_KEEPALIVE is enabled
and the connected socket fails to respond to the keep-alive messages, the connection shall be broken. The default value for
SO_KEEPALIVE is zero, specifying that this capability is turned off.

The SO_LINGER option controls the action of the interface when unsent messages are queued on a socket and a
close() is performed. The details of this option are protocol-specific. If SO_LINGER
is enabled, the system shall block the calling thread during close() until it can
transmit the data or until the end of the interval indicated by the l_linger member, whichever comes first. If SO_LINGER is
not specified, and close() is issued, the system handles the call in a way that allows
the calling thread to continue as quickly as possible. The default value for SO_LINGER is zero, or off, for the l_onoff
element of the option value and zero seconds for the linger time specified by the l_linger element.

The SO_OOBINLINE option is valid only on protocols that support out-of-band data. The SO_OOBINLINE option requests
that out-of-band data be placed in the normal data input queue as received; it is then accessible using the read() or recv() functions without the MSG_OOB flag
set. The default for SO_OOBINLINE is off; that is, for out-of-band data not to be placed in the normal data input queue.

The SO_PROTOCOL option is used only on getsockopt(). When this
option is specified, getsockopt() shall return the socket protocol (for example,
IPPROTO_TCP). SO_PROTOCOL has no default value.

The SO_RCVBUF option requests that the buffer space allocated for receive operations on this socket be set to the
value, in bytes, of the option value. Applications may wish to increase buffer size for high volume connections, or may decrease
buffer size to limit the possible backlog of incoming data. The default value for the SO_RCVBUF option value is
implementation-defined, and may vary by protocol.

The SO_RCVLOWAT option sets the minimum number of bytes to process for socket input operations. In general, receive
calls block until any (non-zero) amount of data is received, then return the smaller of the amount available or the amount
requested. The default value for SO_RCVLOWAT is 1, and does not affect the general case. If SO_RCVLOWAT is set to a larger value,
blocking receive calls normally wait until they have received the smaller of the low water mark value or the requested amount.
Receive calls may still return less than the low water mark if an error occurs, a signal is caught, or the type of data next in the
receive queue is different from that returned (for example, out-of-band data). As mentioned previously, the default value for
SO_RCVLOWAT is 1 byte. It is implementation-defined whether the SO_RCVLOWAT option can be set.

The SO_RCVTIMEO option is an option to set a timeout value for input operations. It accepts a timeval
structure with the number of seconds and microseconds specifying the limit on how long to wait for an input operation to complete.
If a receive operation has blocked for this much time without receiving additional data, it shall return with a partial count or
errno shall be set to [EAGAIN] or [EWOULDBLOCK] if no data were received. The default for this option is the value zero,
which indicates that a receive operation will not time out. It is implementation-defined whether the SO_RCVTIMEO option can be
set.

The SO_REUSEADDR option indicates that the rules used in validating addresses supplied in a bind() should allow reuse of local addresses. Operation of this option is protocol-specific.
The default value for SO_REUSEADDR is off; that is, reuse of local addresses is not permitted.

The SO_SNDBUF option requests that the buffer space allocated for send operations on this socket be set to the
value, in bytes, of the option value. The default value for the SO_SNDBUF option value is implementation-defined, and may vary by
protocol.

The SO_SNDLOWAT option sets the minimum number of bytes to process for socket output operations. Most output
operations process all of the data supplied by the call, delivering data to the protocol for transmission and blocking as necessary
for flow control. Non-blocking output operations process as much data as permitted subject to flow control without blocking, but
process no data if flow control does not allow the smaller of the send low water mark value or the entire request to be processed.
A select() operation testing the ability to write to a socket shall return true only
if the send low water mark could be processed. The default value for SO_SNDLOWAT is implementation-defined and protocol-specific.
It is implementation-defined whether the SO_SNDLOWAT option can be set.

The SO_SNDTIMEO option is an option to set a timeout value for the amount of time that an output function shall
block because flow control prevents data from being sent. As noted in Socket-Level Options, the option
value is a timeval structure with the number of seconds and microseconds specifying the limit on how long to wait for an
output operation to complete. If a send operation has blocked for this much time, it shall return with a partial count or
errno set to [EAGAIN] or [EWOULDBLOCK] if no data were sent. The default for this option is the value zero, which indicates
that a send operation will not time out. It is implementation-defined whether the SO_SNDTIMEO option can be set.

The SO_TYPE option is used only on getsockopt(). When this option
is specified, getsockopt() shall return the type of the socket (for example,
SOCK_STREAM). This option is useful to servers that inherit sockets on start-up. SO_TYPE has no default value.

2.10.17 Use of Sockets for Local UNIX Connections

Support for UNIX domain sockets is mandatory.

UNIX domain sockets provide process-to-process communication in a single system.

2.10.17.1 Headers

The symbolic constant AF_UNIX defined in the <sys/socket.h> header is used to identify the UNIX domain address family. The
<sys/un.h> header contains other definitions used in connection with UNIX
domain sockets. See XBD 14. Headers.

The sockaddr_storage structure defined in <sys/socket.h> shall be large enough to accommodate a sockaddr_un structure
(see the <sys/un.h> header defined in XBD 14. Headers) and shall be aligned at an appropriate boundary so that pointers to it
can be cast as pointers to sockaddr_un structures and used to access the fields of those structures without alignment
problems. When a sockaddr_storage structure is cast as a sockaddr_un structure, the ss_family field maps onto
the sun_family field.

2.10.18 Use of Sockets over Internet Protocols

When a socket is created in the Internet family with a protocol value of zero, the implementation shall use the
protocol listed below for the type of socket created.

SOCK_STREAM
IPPROTO_TCP.
SOCK_DGRAM
IPPROTO_UDP.
SOCK_RAW
[RS]
IPPROTO_RAW.
SOCK_SEQPACKET
Unspecified.

[RS]  A raw interface to IP is available by creating an Internet socket of type SOCK_RAW. The default protocol for type
SOCK_RAW shall be identified in the IP header with the value IPPROTO_RAW. Applications should not use the default protocol when
creating a socket with type SOCK_RAW, but should identify a specific protocol by value. The ICMP control protocol is accessible
from a raw socket by specifying a value of IPPROTO_ICMP for protocol.

2.10.19 Use of Sockets over Internet Protocols Based on IPv4

Support for sockets over Internet protocols based on IPv4 is mandatory. IPv4 is described in RFC 791.

2.10.19.1 Headers

The symbolic constant AF_INET defined in the <sys/socket.h> header is used to identify the IPv4 Internet address family. The
<netinet/in.h> header contains other definitions used in connection with
IPv4 Internet sockets. See XBD 14. Headers.

The sockaddr_storage structure defined in <sys/socket.h> shall be large enough to accommodate a sockaddr_in structure
(see the <netinet/in.h> header defined in XBD 14. Headers) and shall be aligned at an appropriate boundary so that pointers to it
can be cast as pointers to sockaddr_in structures and used to access the fields of those structures without alignment
problems. When a sockaddr_storage structure is cast as a sockaddr_in structure, the ss_family field maps onto
the sin_family field.

2.10.20 Use of Sockets over Internet Protocols Based on IPv6

[IP6]  This section describes extensions to support sockets over Internet protocols based on IPv6. The functionality described
in this section shall be provided on implementations that support the IPV6 option (and the rest of this section is not further
shaded for this option).

IPv6 is described in RFC 8200.

To enable smooth transition from IPv4 to IPv6, the features defined in this section may, in certain circumstances,
also be used in connection with IPv4; see 2.10.20.2 Compatibility with IPv4.

2.10.20.1 Addressing

IPv6 overcomes the addressing limitations of earlier versions by using 128-bit addresses instead of 32-bit
addresses. The IPv6 address architecture is described in RFC 4291.

There are three kinds of IPv6 address:

Unicast

Identifies a single interface.

A unicast address can be global, link-local (designed for use on a single link), or site-local (designed for
systems not connected to the Internet). Link-local and site-local addresses need not be globally unique.

Anycast

Identifies a set of interfaces such that a packet sent to the address can be delivered to any member of the set.

An anycast address is similar to a unicast address; the nodes to which an anycast address is assigned need to be
explicitly configured to know that it is an anycast address.

Multicast

Identifies a set of interfaces such that a packet sent to the address should be delivered to every member of the set.

An application can send multicast datagrams by simply specifying an IPv6 multicast address in the address
argument of sendto(). To receive multicast datagrams, an application needs to join
the multicast group (using setsockopt() with IPV6_JOIN_GROUP) and bind to the
socket the UDP port on which datagrams are to be received. Some applications should also bind the multicast group address to the
socket, to prevent other datagrams destined to that port from being delivered to the socket.

A multicast address can be global, node-local, link-local, site-local, or organization-local.

The following special IPv6 addresses are defined:

Unspecified

An address that is not assigned to any interface and is used to indicate the absence of an address.
Loopback

A unicast address that is not assigned to any interface and can be used by a node to send packets to itself.

Two sets of IPv6 addresses are defined to correspond to IPv4 addresses:

IPv4-compatible addresses

These are assigned to nodes that support IPv6 and can be used when traffic is "tunneled" through IPv4.
IPv4-mapped addresses

These are used to represent IPv4 addresses in IPv6 address format; see 2.10.20.2 Compatibility with
IPv4.

The unspecified address and the loopback address shall not be treated as IPv4-compatible addresses.

2.10.20.2 Compatibility with IPv4

The API provides the ability for IPv6 applications to interoperate with applications using IPv4, by using
IPv4-mapped IPv6 addresses. These addresses can be generated automatically by the getaddrinfo() function when the specified host has only IPv4 addresses.

Applications can use AF_INET6 sockets to open TCP connections to IPv4 nodes, or send UDP packets to IPv4 nodes, by
simply encoding the destination's IPv4 address as an IPv4-mapped IPv6 address, and passing that address, within a
sockaddr_in6 structure, in the connect(), sendto(), or sendmsg() function. When
applications use AF_INET6 sockets to accept TCP connections from IPv4 nodes, or receive UDP packets from IPv4 nodes, the system
shall return the peer's address to the application in the accept(), accept4(), recvfrom(), recvmsg(), or getpeername() function
using a sockaddr_in6 structure encoded this way. If a node has an IPv4 address, then the implementation shall allow
applications to communicate using that address via an AF_INET6 socket. In such a case, the address shall be represented at the API
by the corresponding IPv4-mapped IPv6 address. Also, the implementation may allow an AF_INET6 socket bound to in6addr_any to
receive inbound connections and packets destined to one of the node's IPv4 addresses.

An application can use AF_INET6 sockets to bind to a node's IPv4 address by specifying the address as an
IPv4-mapped IPv6 address in a sockaddr_in6 structure in the bind() function. For
an AF_INET6 socket bound to a node's IPv4 address, the system shall return the address in the getsockname() function as an IPv4-mapped IPv6 address in a sockaddr_in6
structure.

2.10.20.3 Interface Identification

Each local interface is assigned a unique positive integer as a numeric index. Indexes start at 1; zero is not
used. There may be gaps so that there is no current interface for a particular positive index. Each interface also has a unique
implementation-defined name.

2.10.20.4 Options

The following options apply at the IPPROTO_IPV6 level:

IPV6_JOIN_GROUP

When set via setsockopt(), it joins the application to a multicast group on an
interface (identified by its index) and addressed by a given multicast address, enabling packets sent to that address to be read
via the socket. If the interface index is specified as zero, the system selects the interface (for example, by looking up the
address in a routing table and using the resulting interface).

An attempt to read this option using getsockopt() shall result in
an [EOPNOTSUPP] error.

The parameter type of this option is a pointer to an ipv6_mreq structure.

IPV6_LEAVE_GROUP

When set via setsockopt(), it removes the application from the multicast group on
an interface (identified by its index) and addressed by a given multicast address.

An attempt to read this option using getsockopt() shall result in
an [EOPNOTSUPP] error.

The parameter type of this option is a pointer to an ipv6_mreq structure.

IPV6_MULTICAST_HOPS

The value of this option is the hop limit for outgoing multicast IPv6 packets sent via the socket. Its possible values are the same
as those of IPV6_UNICAST_HOPS. If the IPV6_MULTICAST_HOPS option is not set, a value of 1 is assumed. This option can be set via
setsockopt() and read via getsockopt().

The parameter type of this option is a pointer to an int. (Default value: 1)

IPV6_MULTICAST_IF

The index of the interface to be used for outgoing multicast packets. It can be set via setsockopt() and read via getsockopt().
If the interface index is specified as zero, the system selects the interface (for example, by looking up the address in a routing
table and using the resulting interface).

The parameter type of this option is a pointer to an unsigned int. (Default value: 0)

IPV6_MULTICAST_LOOP

This option controls whether outgoing multicast packets should be delivered back to the local application when the sending
interface is itself a member of the destination multicast group. If it is set to 1 they are delivered. If it is set to 0 they are
not. Other values result in an [EINVAL] error. This option can be set via setsockopt() and read via getsockopt().

The parameter type of this option is a pointer to an unsigned int which is used as a Boolean value. (Default
value: 1)

IPV6_UNICAST_HOPS

The value of this option is the hop limit for outgoing unicast IPv6 packets sent via the socket. If the option is not set, or is
set to -1, the system selects a default value. Attempts to set a value less than -1 or greater than 255 shall result in an [EINVAL]
error. This option can be set via setsockopt() and read via getsockopt().

The parameter type of this option is a pointer to an int. (Default value: Unspecified)

IPV6_V6ONLY

This socket option restricts AF_INET6 sockets to IPv6 communications only. AF_INET6 sockets may be used for both IPv4 and IPv6
communications. Some applications may want to restrict their use of an AF_INET6 socket to IPv6 communications only. For these
applications, the IPv6_V6ONLY socket option is defined. When this option is turned on, the socket can be used to send and receive
IPv6 packets only. This is an IPPROTO_IPV6-level option.

The parameter type of this option is a pointer to an int which is used as a Boolean value. (Default value:
0)

An [EOPNOTSUPP] error shall result if IPV6_JOIN_GROUP or IPV6_LEAVE_GROUP is used with getsockopt().

2.10.20.5 Headers

The symbolic constant AF_INET6 is defined in the <sys/socket.h> header to identify the IPv6 Internet address family. See XBD
14. Headers.

The sockaddr_storage structure defined in <sys/socket.h> shall be large enough to accommodate a sockaddr_in6
structure (see the <netinet/in.h> header defined in XBD 14. Headers) and shall be aligned at an appropriate boundary so that pointers to it
can be cast as pointers to sockaddr_in6 structures and used to access the fields of those structures without alignment
problems. When a sockaddr_storage structure is cast as a sockaddr_in6 structure, the ss_family field maps onto
the sin6_family field.

The <netinet/in.h>, <arpa/inet.h>, and <netdb.h>
headers contain other definitions used in connection with IPv6 Internet sockets; see XBD 14. Headers.

2.11 Data Types

2.11.1 Defined Types

All of the data types used by various functions are defined by the implementation. The following table describes
some of these types. Other types referenced in the description of a function, not mentioned here, can be found in the appropriate
header for that function.

Defined Type

Description

cc_t

Type used for terminal special characters.

clock_t

Integer or real-floating type used for processor times, as defined in the ISO C standard.

clockid_t

Used for clock ID type in some timer functions.

dev_t

Integer type used for device numbers.

DIR

Type representing a directory stream.

div_t

Structure type returned by the div() function.

FILE

Structure containing information about a file.

glob_t

Structure type used in pathname pattern matching.

fpos_t

Type containing all information needed to specify uniquely every position within a file.

gid_t

Integer type used for group IDs.

iconv_t

Type used for conversion descriptors.

id_t

Integer type used as a general identifier; can be used to contain at least the largest of a pid_t,
uid_t, or gid_t.

ino_t

Unsigned integer type used for file serial numbers.

key_t

Arithmetic type used for XSI interprocess communication.

ldiv_t

Structure type returned by the ldiv() function.

mode_t

Integer type used for file attributes.

mqd_t

Used for message queue descriptors.

nfds_t

Integer type used for the number of file descriptors.

nlink_t

Integer type used for link counts.

off_t

Signed integer type used for file sizes.

pid_t

Signed integer type used for process and process group IDs.

pthread_attr_t

Used to identify a thread attribute object.

pthread_cond_t, cnd_t

Used for condition variables.

pthread_condattr_t

Used to identify a condition attribute object.

pthread_key_t, tss_t

Used for thread-specific data keys.

pthread_mutex_t, mtx_t

Used for mutexes.

pthread_mutexattr_t

Used to identify a mutex attribute object.

pthread_once_t, once_flag

Used for dynamic package initialization.

pthread_rwlock_t

Used for read-write locks.

pthread_rwlockattr_t

Used for read-write lock attributes.

pthread_t, thrd_t

Used to identify a thread.

ptrdiff_t

Signed integer type of the result of subtracting two pointers.

reclen_t

Unsigned integer type used for directory entry lengths.

regex_t

Structure type used in regular expression matching.

regmatch_t

Structure type used in regular expression matching.

rlim_t

Unsigned integer type used for limit values, to which objects of type int and off_t can be cast
without loss of value.

sem_t

Type used in performing semaphore operations.

sig_atomic_t

Possibly volatile-qualified integer type of an object that can be accessed as an atomic entity, even in the
presence of asynchronous interrupts.

sigset_t

Integer or structure type of an object used to represent sets of signals.

size_t

Unsigned integer type used for size of objects.

speed_t

Type used for terminal baud rates.

ssize_t

Signed integer type used for a count of bytes or an error indication.

suseconds_t

Signed integer type used for time in microseconds.

tcflag_t

Type used for terminal modes.

time_t

Integer type used for time in seconds, as defined in the ISO C standard.

timer_t

Used for timer ID returned by the timer_create() function.

uid_t

Integer type used for user IDs.

va_list

Type used for traversing variable argument lists.

wchar_t

Integer type whose range of values can represent distinct codes for all members of the largest extended character
set specified by the supported locales.

wctype_t

Scalar type which represents a character class descriptor.

wint_t

Integer type capable of storing any valid value of wchar_t or WEOF.

wordexp_t

Structure type used in word expansion.

2.11.2 The char Type

The type char is defined as a single byte; see XBD 3.
Definitions (Byte and Character).

2.12 Status Information

Status information is data associated with a process detailing a change in the state of the process. It shall
consist of:

The state the process transitioned into (stopped, continued, or terminated)

The information necessary to populate the siginfo_t structure provided by waitid()

If the new state is terminated:

The low-order 8 bits of the status argument that the process passed to _Exit(), _exit(), or exit(), or the low-order 8 bits of the value the process returned from main()

Note that these 8 bits are part of the complete value that is used to set the si_status member of the
siginfo_t structure provided by waitid()

Whether the process terminated due to the receipt of a signal that was not caught and, if so, the number of the
signal that caused the termination of the process

If the new state is stopped:

The number of the signal that caused the process to stop

A process might not have any status information (such as immediately after a process has started).

Status information for a process shall be generated (made available to the parent process) when the process stops,
continues, or terminates except in the following case:

If the parent process sets the action for the SIGCHLD signal to SIG_IGN, or if the parent sets the SA_NOCLDWAIT
flag for the SIGCHLD signal action, process termination shall not generate new status information but shall cause any existing
status information for the process to be discarded.

If new status information is generated, and the process already had status information, the existing status
information shall be discarded and replaced with the new status information.

Only the process' parent process can obtain the process' status information. The parent obtains a child's status
information by calling wait(), waitid(),
or waitpid(). Except when waitid() is
called with the WNOWAIT flag set in the options argument, the status information obtained by a wait function shall be
consumed (discarded) by that wait function; no two calls to wait(), waitid() (without WNOWAIT), or waitpid() shall
obtain the same status information.

When status information becomes available to the parent process and more than one thread in the parent process is
waiting for the status information (blocked in a call to wait(), waitid(), or waitpid() with arguments that
would match the status information):

If none of the matching threads is in a call to waitid() with the
WNOWAIT flag set in the options argument, the thread that obtains the status information is unspecified.

Otherwise (at least one of the matching threads is in a call to waitid() with the WNOWAIT flag set), the matching thread or threads that obtain the status
information is unspecified except that at least one of the matching threads shall obtain the status information and at most one of
the matching threads that are not calling waitid() with the WNOWAIT flag set shall
obtain it.

Footnotes

1. The functions in the table are not shaded to denote applicable options. Individual
reference pages should be consulted. †

When the cmd argument is F_SETLKW or F_OFD_SETLKW. †† When the function argument is F_LOCK. ††† For any value of the
cmd argument.

return to top of page

UNIX® is a registered Trademark of The Open Group.

POSIX™ is a Trademark of The IEEE.

Copyright © 2001-2024 The IEEE and The Open Group, All Rights Reserved

[ Main Index | XBD | XSH | XCU | XRAT
]

<<<
Previous
Home
Next
>>>
