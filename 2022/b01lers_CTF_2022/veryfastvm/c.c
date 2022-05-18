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
