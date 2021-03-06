# parity(170pts)
Check your parity.

# Solution
配布されるバイナリは入力したバイト列をshellcodeとして実行してくれる。
なので、よく見かけるような`syscall(rax: 59, rdi: &"/bin/sh", rdx: NULL, rsi: NULL)`の内容のバイト列を入力すればよい。

しかしshellcodeには条件があり、shellcodeのバイト列は偶数奇数が交互に現れないといけない。

ところでLinuxのx86_64のsyscall命令は`0f 05`であり一つの命令を見ても偶奇交互の条件を満たさないことに気づくので何かしらEncode, Decodeの処理を入れることで対処しなければならない。
私の解法では偶奇交互の条件を満たすようにバイト列を並べて置き、適切な命令となるようにバイト列を修正する方針で行った。

syscall命令は、`0f 04`とバイト列を並べて置き`04`に`+1`することで`0f 05`(syscall命令)を作成している。

"/bin/sh"の文字列に関しても同様に、`2f 62 69 6e 2f 72 67 00`とバイト列を並べて置き`72`と`67`をそれぞれ`+1`することで`2f 62 69 6e 2f 73 68 00`("/bin/sh\x00"の文字列)を作成している。

`+1`する処理は`add BYTE PTR[rcx+偶数の即値], bl`命令を使い`00 59 偶数の即値`という偶奇偶の順番のバイト列で表現している。

このような処理を疑似コードで表すと以下のようになる。
データを修正した後、各レジスタを設定し、syscall命令を実行する流れである。

```
[syscallの素データ]をadd命令を使い修正
[/bin/shの素データ]をadd命令を使い修正
rdi = &"/bin/sh"
rdx = 0
rax = 59
rsi = 0
[syscallの素データ]
[/bin/shの素データ]
```

以上のような処理内容を偶奇が交互に現れるようなバイト列で表現すれば良いが、1命令あたりのバイト数が1,2,3byteといったの短い命令を使用したとしても偶奇交互に現れるように調整するためにパディングのようなバイト列が必要になる。そのような場合、

奇数のバイト列が必要な箇所では`push rcx`命令を使用し`51`という奇数バイトで表現

偶数のバイト列が必要な箇所では`nop`命令を使用し`90`という偶数バイトで表現

することで対処している。

