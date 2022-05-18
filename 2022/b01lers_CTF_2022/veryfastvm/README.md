問題として配布されるプログラムファイルは [cpu.py](./cpu.py) であるが変数名が分かりにくかったため、[cpu_patched.py](./cpu_patched.py)のように変数名を分かりやすいように変更した。(変数名の意味が正しいかは保証しない。)


プログラムを読むと、`flag.txt`の中身を見るためには以下の2つの条件を満たした上で`magic`命令を呼び出すことが必要である
1. cpuのreset counterを2にする(161行目)
2. registerのr0, r1, r2, r3に129行目で生成されている乱数値を設定する(162行目)

条件1を満たすためには、`reset`命令を呼び出せば良い。(138行目)

条件2を満たすためには、初回起動(run)時に乱数値がmemory[0:4]に保存されているので、memory[0:4]の内容をr0~r3に保存すればよい。


ここで問題となるのは、条件1を満たすためにreset命令を呼び出すとregisterの値、memoryの値、cacheに保存されている値、instruction counterを初期化してしまうということである。

条件2を満たすためにどこかに乱数値の情報を保存しておきたいが、条件1を満たすためにreset命令を呼び出すとregisterの値とmemoryの値とcacheに保存されている値が初期化されてしまうので乱数値の情報を保存することができない。

これでは条件1と条件2を同時に満たすことができないのではないかと思ってしまうが、reset命令の処理内容をしっかり読んでみるとcacheの初期化の部分で、`cacheの値は0で初期化をするがcacheのindex値は初期化を行っていない`という問題があることに気がつく。(137行目)

この問題点を利用すると、`乱数値をcacheのindex値情報として保存した状態でreset命令を呼び出し、cacheのindex値から乱数値を復元する`ことで条件1と条件2と満たすことができる。

以下の疑似コードのような処理をアセンブリ命令として書き直したのが[答え](./poc.txt)である。
magic命令実行後はregisterにflagの値が整数値として保存されているので文字列に変換すれば良い。

```
if(memory[0] != 0){ // 一度resetされているか
    // 乱数値をcacheのindex情報として保存
    for(int i=0;i<4;i++){
    	int t = memory[i];
        for(int j=0;j<32;j++){
            if(t&(1<<j)){
                cache[32+i*32+j] = 0; // movfrom命令
                memory[32+i*32+j] = 0; // movfrom命令
            }
        }
    }

    reset();
}else{
    // cacheのindex値から乱数値を復元
    for(int i=0;i<4;i++){
        int t = 0;
        for(int j=0;j<32;j++){
            if(exist(cache[32+i*32+j])){ // if( consume_time_movfrom == 3 )
                t += (1<<j);
            }
        }
    }

    magic(memory[0], memory[1], memory[2], memory[3]);
}

```

なお、cacheのindex値が存在しているかどうかによってmovfrom命令の実行時間が異なるというサイドチャネル攻撃で使われそうな方法によって、cacheのindex値が存在しているかを判別しcacheのindex値から乱数値を復元している。