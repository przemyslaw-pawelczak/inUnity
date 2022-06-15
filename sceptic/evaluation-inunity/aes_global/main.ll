; ModuleID = 'main.c'
source_filename = "main.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@test_encrypt_ecb_verbose.key = private unnamed_addr constant [16 x i8] c"+~\15\16(\AE\D2\A6\AB\F7\15\88\09\CFO<", align 16
@test_encrypt_ecb_verbose.plain_text = private unnamed_addr constant [64 x i8] c"k\C1\BE\E2.@\9F\96\E9=~\11s\93\17*\AE-\8AW\1E\03\AC\9C\9E\B7o\ACE\AF\8EQ0\C8\1CF\A3\5C\E4\11\E5\FB\C1\19\1A\0AR\EF\F6\9F$E\DFO\9B\17\AD+A{\E6l7\10", align 16
@.str = private unnamed_addr constant [23 x i8] c"ECB encrypt verbose:\0A\0A\00", align 1
@.str.1 = private unnamed_addr constant [13 x i8] c"plain text:\0A\00", align 1
@.str.2 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@.str.3 = private unnamed_addr constant [6 x i8] c"key:\0A\00", align 1
@.str.4 = private unnamed_addr constant [13 x i8] c"ciphertext:\0A\00", align 1
@.str.5 = private unnamed_addr constant [5 x i8] c"%.2x\00", align 1
@test_encrypt_ecb.key = private unnamed_addr constant [16 x i8] c"+~\15\16(\AE\D2\A6\AB\F7\15\88\09\CFO<", align 16
@test_encrypt_ecb.in = private unnamed_addr constant [16 x i8] c"k\C1\BE\E2.@\9F\96\E9=~\11s\93\17*", align 16
@test_encrypt_ecb.out = private unnamed_addr constant [16 x i8] c":\D7{\B4\0Dz6`\A8\9E\CA\F3$f\EF\97", align 16
@.str.6 = private unnamed_addr constant [14 x i8] c"ECB decrypt: \00", align 1
@.str.7 = private unnamed_addr constant [10 x i8] c"SUCCESS!\0A\00", align 1
@.str.8 = private unnamed_addr constant [10 x i8] c"FAILURE!\0A\00", align 1
@test_decrypt_cbc.key = private unnamed_addr constant [16 x i8] c"+~\15\16(\AE\D2\A6\AB\F7\15\88\09\CFO<", align 16
@test_decrypt_cbc.iv = private unnamed_addr constant [16 x i8] c"\00\01\02\03\04\05\06\07\08\09\0A\0B\0C\0D\0E\0F", align 16
@test_decrypt_cbc.in = private unnamed_addr constant [64 x i8] c"vI\AB\AC\81\19\B2F\CE\E9\8E\9B\12\E9\19}P\86\CB\9BPr\19\EE\95\DB\11:\91vx\B2s\BE\D6\B8\E3\C1t;q\16\E6\9E\22\22\95\16?\F1\CA\A1h\1F\AC\09\12\0E\CA0u\86\E1\A7", align 16
@test_decrypt_cbc.out = private unnamed_addr constant [64 x i8] c"k\C1\BE\E2.@\9F\96\E9=~\11s\93\17*\AE-\8AW\1E\03\AC\9C\9E\B7o\ACE\AF\8EQ0\C8\1CF\A3\5C\E4\11\E5\FB\C1\19\1A\0AR\EF\F6\9F$E\DFO\9B\17\AD+A{\E6l7\10", align 16
@.str.9 = private unnamed_addr constant [14 x i8] c"CBC decrypt: \00", align 1
@test_encrypt_cbc.key = private unnamed_addr constant [16 x i8] c"+~\15\16(\AE\D2\A6\AB\F7\15\88\09\CFO<", align 16
@test_encrypt_cbc.iv = private unnamed_addr constant [16 x i8] c"\00\01\02\03\04\05\06\07\08\09\0A\0B\0C\0D\0E\0F", align 16
@test_encrypt_cbc.in = private unnamed_addr constant [64 x i8] c"k\C1\BE\E2.@\9F\96\E9=~\11s\93\17*\AE-\8AW\1E\03\AC\9C\9E\B7o\ACE\AF\8EQ0\C8\1CF\A3\5C\E4\11\E5\FB\C1\19\1A\0AR\EF\F6\9F$E\DFO\9B\17\AD+A{\E6l7\10", align 16
@test_encrypt_cbc.out = private unnamed_addr constant [64 x i8] c"vI\AB\AC\81\19\B2F\CE\E9\8E\9B\12\E9\19}P\86\CB\9BPr\19\EE\95\DB\11:\91vx\B2s\BE\D6\B8\E3\C1t;q\16\E6\9E\22\22\95\16?\F1\CA\A1h\1F\AC\09\12\0E\CA0u\86\E1\A7", align 16
@.str.10 = private unnamed_addr constant [14 x i8] c"CBC encrypt: \00", align 1
@test_decrypt_ecb.key = private unnamed_addr constant [16 x i8] c"+~\15\16(\AE\D2\A6\AB\F7\15\88\09\CFO<", align 16
@test_decrypt_ecb.in = private unnamed_addr constant [16 x i8] c":\D7{\B4\0Dz6`\A8\9E\CA\F3$f\EF\97", align 16
@test_decrypt_ecb.out = private unnamed_addr constant [16 x i8] c"k\C1\BE\E2.@\9F\96\E9=~\11s\93\17*", align 16

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 !dbg !15 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @test_encrypt_cbc(), !dbg !19
  %2 = call i32 (...) @checkpoint(), !dbg !20
  call void @test_decrypt_cbc(), !dbg !21
  %3 = call i32 (...) @checkpoint(), !dbg !22
  call void @test_decrypt_ecb(), !dbg !23
  %4 = call i32 (...) @checkpoint(), !dbg !24
  call void @test_encrypt_ecb(), !dbg !25
  %5 = call i32 (...) @checkpoint(), !dbg !26
  call void @test_encrypt_ecb_verbose(), !dbg !27
  %6 = call i32 (...) @checkpoint(), !dbg !28
  ret i32 0, !dbg !29
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @test_encrypt_cbc() #0 !dbg !30 {
  %1 = alloca [16 x i8], align 16
  %2 = alloca [16 x i8], align 16
  %3 = alloca [64 x i8], align 16
  %4 = alloca [64 x i8], align 16
  %5 = alloca [64 x i8], align 16
  call void @llvm.dbg.declare(metadata [16 x i8]* %1, metadata !33, metadata !DIExpression()), !dbg !37
  %6 = bitcast [16 x i8]* %1 to i8*, !dbg !37
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %6, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_encrypt_cbc.key, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !37
  call void @llvm.dbg.declare(metadata [16 x i8]* %2, metadata !38, metadata !DIExpression()), !dbg !39
  %7 = bitcast [16 x i8]* %2 to i8*, !dbg !39
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %7, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_encrypt_cbc.iv, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !39
  call void @llvm.dbg.declare(metadata [64 x i8]* %3, metadata !40, metadata !DIExpression()), !dbg !44
  %8 = bitcast [64 x i8]* %3 to i8*, !dbg !44
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %8, i8* getelementptr inbounds ([64 x i8], [64 x i8]* @test_encrypt_cbc.in, i32 0, i32 0), i64 64, i32 16, i1 false), !dbg !44
  call void @llvm.dbg.declare(metadata [64 x i8]* %4, metadata !45, metadata !DIExpression()), !dbg !46
  %9 = bitcast [64 x i8]* %4 to i8*, !dbg !46
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %9, i8* getelementptr inbounds ([64 x i8], [64 x i8]* @test_encrypt_cbc.out, i32 0, i32 0), i64 64, i32 16, i1 false), !dbg !46
  call void @llvm.dbg.declare(metadata [64 x i8]* %5, metadata !47, metadata !DIExpression()), !dbg !48
  %10 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !49
  %11 = getelementptr inbounds [64 x i8], [64 x i8]* %3, i32 0, i32 0, !dbg !50
  %12 = getelementptr inbounds [16 x i8], [16 x i8]* %1, i32 0, i32 0, !dbg !51
  %13 = getelementptr inbounds [16 x i8], [16 x i8]* %2, i32 0, i32 0, !dbg !52
  call void @AES128_CBC_encrypt_buffer(i8* %10, i8* %11, i32 64, i8* %12, i8* %13), !dbg !53
  %14 = call i32 (...) @checkpoint(), !dbg !54
  %15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.10, i32 0, i32 0)), !dbg !55
  %16 = getelementptr inbounds [64 x i8], [64 x i8]* %4, i32 0, i32 0, !dbg !56
  %17 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !58
  %18 = call i32 @strncmp(i8* %16, i8* %17, i64 64) #5, !dbg !59
  %19 = icmp eq i32 0, %18, !dbg !60
  br i1 %19, label %20, label %22, !dbg !61

; <label>:20:                                     ; preds = %0
  %21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.7, i32 0, i32 0)), !dbg !62
  br label %24, !dbg !64

; <label>:22:                                     ; preds = %0
  %23 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.8, i32 0, i32 0)), !dbg !65
  br label %24

; <label>:24:                                     ; preds = %22, %20
  ret void, !dbg !67
}

declare i32 @checkpoint(...) #1

; Function Attrs: noinline nounwind optnone uwtable
define internal void @test_decrypt_cbc() #0 !dbg !68 {
  %1 = alloca [16 x i8], align 16
  %2 = alloca [16 x i8], align 16
  %3 = alloca [64 x i8], align 16
  %4 = alloca [64 x i8], align 16
  %5 = alloca [64 x i8], align 16
  call void @llvm.dbg.declare(metadata [16 x i8]* %1, metadata !69, metadata !DIExpression()), !dbg !70
  %6 = bitcast [16 x i8]* %1 to i8*, !dbg !70
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %6, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_decrypt_cbc.key, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !70
  call void @llvm.dbg.declare(metadata [16 x i8]* %2, metadata !71, metadata !DIExpression()), !dbg !72
  %7 = bitcast [16 x i8]* %2 to i8*, !dbg !72
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %7, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_decrypt_cbc.iv, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !72
  call void @llvm.dbg.declare(metadata [64 x i8]* %3, metadata !73, metadata !DIExpression()), !dbg !74
  %8 = bitcast [64 x i8]* %3 to i8*, !dbg !74
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %8, i8* getelementptr inbounds ([64 x i8], [64 x i8]* @test_decrypt_cbc.in, i32 0, i32 0), i64 64, i32 16, i1 false), !dbg !74
  call void @llvm.dbg.declare(metadata [64 x i8]* %4, metadata !75, metadata !DIExpression()), !dbg !76
  %9 = bitcast [64 x i8]* %4 to i8*, !dbg !76
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %9, i8* getelementptr inbounds ([64 x i8], [64 x i8]* @test_decrypt_cbc.out, i32 0, i32 0), i64 64, i32 16, i1 false), !dbg !76
  call void @llvm.dbg.declare(metadata [64 x i8]* %5, metadata !77, metadata !DIExpression()), !dbg !78
  %10 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !79
  %11 = getelementptr inbounds i8, i8* %10, i64 0, !dbg !80
  %12 = getelementptr inbounds [64 x i8], [64 x i8]* %3, i32 0, i32 0, !dbg !81
  %13 = getelementptr inbounds i8, i8* %12, i64 0, !dbg !82
  %14 = getelementptr inbounds [16 x i8], [16 x i8]* %1, i32 0, i32 0, !dbg !83
  %15 = getelementptr inbounds [16 x i8], [16 x i8]* %2, i32 0, i32 0, !dbg !84
  call void @AES128_CBC_decrypt_buffer(i8* %11, i8* %13, i32 16, i8* %14, i8* %15), !dbg !85
  %16 = call i32 (...) @checkpoint(), !dbg !86
  %17 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !87
  %18 = getelementptr inbounds i8, i8* %17, i64 16, !dbg !88
  %19 = getelementptr inbounds [64 x i8], [64 x i8]* %3, i32 0, i32 0, !dbg !89
  %20 = getelementptr inbounds i8, i8* %19, i64 16, !dbg !90
  call void @AES128_CBC_decrypt_buffer(i8* %18, i8* %20, i32 16, i8* null, i8* null), !dbg !91
  %21 = call i32 (...) @checkpoint(), !dbg !92
  %22 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !93
  %23 = getelementptr inbounds i8, i8* %22, i64 32, !dbg !94
  %24 = getelementptr inbounds [64 x i8], [64 x i8]* %3, i32 0, i32 0, !dbg !95
  %25 = getelementptr inbounds i8, i8* %24, i64 32, !dbg !96
  call void @AES128_CBC_decrypt_buffer(i8* %23, i8* %25, i32 16, i8* null, i8* null), !dbg !97
  %26 = call i32 (...) @checkpoint(), !dbg !98
  %27 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !99
  %28 = getelementptr inbounds i8, i8* %27, i64 48, !dbg !100
  %29 = getelementptr inbounds [64 x i8], [64 x i8]* %3, i32 0, i32 0, !dbg !101
  %30 = getelementptr inbounds i8, i8* %29, i64 48, !dbg !102
  call void @AES128_CBC_decrypt_buffer(i8* %28, i8* %30, i32 16, i8* null, i8* null), !dbg !103
  %31 = call i32 (...) @checkpoint(), !dbg !104
  %32 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.9, i32 0, i32 0)), !dbg !105
  %33 = getelementptr inbounds [64 x i8], [64 x i8]* %4, i32 0, i32 0, !dbg !106
  %34 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !108
  %35 = call i32 @strncmp(i8* %33, i8* %34, i64 64) #5, !dbg !109
  %36 = icmp eq i32 0, %35, !dbg !110
  br i1 %36, label %37, label %39, !dbg !111

; <label>:37:                                     ; preds = %0
  %38 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.7, i32 0, i32 0)), !dbg !112
  br label %41, !dbg !114

; <label>:39:                                     ; preds = %0
  %40 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.8, i32 0, i32 0)), !dbg !115
  br label %41

; <label>:41:                                     ; preds = %39, %37
  ret void, !dbg !117
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @test_decrypt_ecb() #0 !dbg !118 {
  %1 = alloca [16 x i8], align 16
  %2 = alloca [16 x i8], align 16
  %3 = alloca [16 x i8], align 16
  %4 = alloca [16 x i8], align 16
  call void @llvm.dbg.declare(metadata [16 x i8]* %1, metadata !119, metadata !DIExpression()), !dbg !120
  %5 = bitcast [16 x i8]* %1 to i8*, !dbg !120
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %5, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_decrypt_ecb.key, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !120
  call void @llvm.dbg.declare(metadata [16 x i8]* %2, metadata !121, metadata !DIExpression()), !dbg !122
  %6 = bitcast [16 x i8]* %2 to i8*, !dbg !122
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %6, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_decrypt_ecb.in, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !122
  call void @llvm.dbg.declare(metadata [16 x i8]* %3, metadata !123, metadata !DIExpression()), !dbg !124
  %7 = bitcast [16 x i8]* %3 to i8*, !dbg !124
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %7, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_decrypt_ecb.out, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !124
  call void @llvm.dbg.declare(metadata [16 x i8]* %4, metadata !125, metadata !DIExpression()), !dbg !126
  %8 = getelementptr inbounds [16 x i8], [16 x i8]* %2, i32 0, i32 0, !dbg !127
  %9 = getelementptr inbounds [16 x i8], [16 x i8]* %1, i32 0, i32 0, !dbg !128
  %10 = getelementptr inbounds [16 x i8], [16 x i8]* %4, i32 0, i32 0, !dbg !129
  call void @AES128_ECB_decrypt(i8* %8, i8* %9, i8* %10), !dbg !130
  %11 = call i32 (...) @checkpoint(), !dbg !131
  %12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.6, i32 0, i32 0)), !dbg !132
  %13 = getelementptr inbounds [16 x i8], [16 x i8]* %3, i32 0, i32 0, !dbg !133
  %14 = getelementptr inbounds [16 x i8], [16 x i8]* %4, i32 0, i32 0, !dbg !135
  %15 = call i32 @strncmp(i8* %13, i8* %14, i64 16) #5, !dbg !136
  %16 = icmp eq i32 0, %15, !dbg !137
  br i1 %16, label %17, label %19, !dbg !138

; <label>:17:                                     ; preds = %0
  %18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.7, i32 0, i32 0)), !dbg !139
  br label %21, !dbg !141

; <label>:19:                                     ; preds = %0
  %20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.8, i32 0, i32 0)), !dbg !142
  br label %21

; <label>:21:                                     ; preds = %19, %17
  ret void, !dbg !144
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @test_encrypt_ecb() #0 !dbg !145 {
  %1 = alloca [16 x i8], align 16
  %2 = alloca [16 x i8], align 16
  %3 = alloca [16 x i8], align 16
  %4 = alloca [16 x i8], align 16
  call void @llvm.dbg.declare(metadata [16 x i8]* %1, metadata !146, metadata !DIExpression()), !dbg !147
  %5 = bitcast [16 x i8]* %1 to i8*, !dbg !147
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %5, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_encrypt_ecb.key, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !147
  call void @llvm.dbg.declare(metadata [16 x i8]* %2, metadata !148, metadata !DIExpression()), !dbg !149
  %6 = bitcast [16 x i8]* %2 to i8*, !dbg !149
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %6, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_encrypt_ecb.in, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !149
  call void @llvm.dbg.declare(metadata [16 x i8]* %3, metadata !150, metadata !DIExpression()), !dbg !151
  %7 = bitcast [16 x i8]* %3 to i8*, !dbg !151
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %7, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_encrypt_ecb.out, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !151
  call void @llvm.dbg.declare(metadata [16 x i8]* %4, metadata !152, metadata !DIExpression()), !dbg !153
  %8 = getelementptr inbounds [16 x i8], [16 x i8]* %2, i32 0, i32 0, !dbg !154
  %9 = getelementptr inbounds [16 x i8], [16 x i8]* %1, i32 0, i32 0, !dbg !155
  %10 = getelementptr inbounds [16 x i8], [16 x i8]* %4, i32 0, i32 0, !dbg !156
  call void @AES128_ECB_encrypt(i8* %8, i8* %9, i8* %10), !dbg !157
  %11 = call i32 (...) @checkpoint(), !dbg !158
  %12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.6, i32 0, i32 0)), !dbg !159
  %13 = getelementptr inbounds [16 x i8], [16 x i8]* %3, i32 0, i32 0, !dbg !160
  %14 = getelementptr inbounds [16 x i8], [16 x i8]* %4, i32 0, i32 0, !dbg !162
  %15 = call i32 @strncmp(i8* %13, i8* %14, i64 16) #5, !dbg !163
  %16 = icmp eq i32 0, %15, !dbg !164
  br i1 %16, label %17, label %19, !dbg !165

; <label>:17:                                     ; preds = %0
  %18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.7, i32 0, i32 0)), !dbg !166
  br label %21, !dbg !168

; <label>:19:                                     ; preds = %0
  %20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.8, i32 0, i32 0)), !dbg !169
  br label %21

; <label>:21:                                     ; preds = %19, %17
  ret void, !dbg !171
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @test_encrypt_ecb_verbose() #0 !dbg !172 {
  %1 = alloca i8, align 1
  %2 = alloca [64 x i8], align 16
  %3 = alloca [64 x i8], align 16
  %4 = alloca [16 x i8], align 16
  %5 = alloca [64 x i8], align 16
  call void @llvm.dbg.declare(metadata i8* %1, metadata !173, metadata !DIExpression()), !dbg !174
  call void @llvm.dbg.declare(metadata [64 x i8]* %2, metadata !175, metadata !DIExpression()), !dbg !176
  call void @llvm.dbg.declare(metadata [64 x i8]* %3, metadata !177, metadata !DIExpression()), !dbg !178
  call void @llvm.dbg.declare(metadata [16 x i8]* %4, metadata !179, metadata !DIExpression()), !dbg !180
  %6 = bitcast [16 x i8]* %4 to i8*, !dbg !180
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %6, i8* getelementptr inbounds ([16 x i8], [16 x i8]* @test_encrypt_ecb_verbose.key, i32 0, i32 0), i64 16, i32 16, i1 false), !dbg !180
  call void @llvm.dbg.declare(metadata [64 x i8]* %5, metadata !181, metadata !DIExpression()), !dbg !182
  %7 = bitcast [64 x i8]* %5 to i8*, !dbg !182
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %7, i8* getelementptr inbounds ([64 x i8], [64 x i8]* @test_encrypt_ecb_verbose.plain_text, i32 0, i32 0), i64 64, i32 16, i1 false), !dbg !182
  %8 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0, !dbg !183
  call void @llvm.memset.p0i8.i64(i8* %8, i8 0, i64 64, i32 16, i1 false), !dbg !183
  %9 = getelementptr inbounds [64 x i8], [64 x i8]* %3, i32 0, i32 0, !dbg !184
  call void @llvm.memset.p0i8.i64(i8* %9, i8 0, i64 64, i32 16, i1 false), !dbg !184
  %10 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([23 x i8], [23 x i8]* @.str, i32 0, i32 0)), !dbg !185
  %11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([13 x i8], [13 x i8]* @.str.1, i32 0, i32 0)), !dbg !186
  store i8 0, i8* %1, align 1, !dbg !187
  br label %12, !dbg !189

; <label>:12:                                     ; preds = %24, %0
  %13 = load i8, i8* %1, align 1, !dbg !190
  %14 = zext i8 %13 to i32, !dbg !190
  %15 = icmp slt i32 %14, 4, !dbg !192
  br i1 %15, label %16, label %27, !dbg !193

; <label>:16:                                     ; preds = %12
  %17 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !194
  %18 = load i8, i8* %1, align 1, !dbg !196
  %19 = zext i8 %18 to i32, !dbg !196
  %20 = mul nsw i32 %19, 16, !dbg !197
  %21 = sext i32 %20 to i64, !dbg !198
  %22 = getelementptr inbounds i8, i8* %17, i64 %21, !dbg !198
  call void @phex(i8* %22), !dbg !199
  %23 = call i32 (...) @checkpoint(), !dbg !200
  br label %24, !dbg !201

; <label>:24:                                     ; preds = %16
  %25 = load i8, i8* %1, align 1, !dbg !202
  %26 = add i8 %25, 1, !dbg !202
  store i8 %26, i8* %1, align 1, !dbg !202
  br label %12, !dbg !203, !llvm.loop !204

; <label>:27:                                     ; preds = %12
  %28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2, i32 0, i32 0)), !dbg !206
  %29 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.3, i32 0, i32 0)), !dbg !207
  %30 = getelementptr inbounds [16 x i8], [16 x i8]* %4, i32 0, i32 0, !dbg !208
  call void @phex(i8* %30), !dbg !209
  %31 = call i32 (...) @checkpoint(), !dbg !210
  %32 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2, i32 0, i32 0)), !dbg !211
  %33 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([13 x i8], [13 x i8]* @.str.4, i32 0, i32 0)), !dbg !212
  store i8 0, i8* %1, align 1, !dbg !213
  br label %34, !dbg !215

; <label>:34:                                     ; preds = %60, %27
  %35 = load i8, i8* %1, align 1, !dbg !216
  %36 = zext i8 %35 to i32, !dbg !216
  %37 = icmp slt i32 %36, 4, !dbg !218
  br i1 %37, label %38, label %63, !dbg !219

; <label>:38:                                     ; preds = %34
  %39 = getelementptr inbounds [64 x i8], [64 x i8]* %5, i32 0, i32 0, !dbg !220
  %40 = load i8, i8* %1, align 1, !dbg !222
  %41 = zext i8 %40 to i32, !dbg !222
  %42 = mul nsw i32 %41, 16, !dbg !223
  %43 = sext i32 %42 to i64, !dbg !224
  %44 = getelementptr inbounds i8, i8* %39, i64 %43, !dbg !224
  %45 = getelementptr inbounds [16 x i8], [16 x i8]* %4, i32 0, i32 0, !dbg !225
  %46 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0, !dbg !226
  %47 = load i8, i8* %1, align 1, !dbg !227
  %48 = zext i8 %47 to i32, !dbg !227
  %49 = mul nsw i32 %48, 16, !dbg !228
  %50 = sext i32 %49 to i64, !dbg !229
  %51 = getelementptr inbounds i8, i8* %46, i64 %50, !dbg !229
  call void @AES128_ECB_encrypt(i8* %44, i8* %45, i8* %51), !dbg !230
  %52 = call i32 (...) @checkpoint(), !dbg !231
  %53 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0, !dbg !232
  %54 = load i8, i8* %1, align 1, !dbg !233
  %55 = zext i8 %54 to i32, !dbg !233
  %56 = mul nsw i32 %55, 16, !dbg !234
  %57 = sext i32 %56 to i64, !dbg !235
  %58 = getelementptr inbounds i8, i8* %53, i64 %57, !dbg !235
  call void @phex(i8* %58), !dbg !236
  %59 = call i32 (...) @checkpoint(), !dbg !237
  br label %60, !dbg !238

; <label>:60:                                     ; preds = %38
  %61 = load i8, i8* %1, align 1, !dbg !239
  %62 = add i8 %61, 1, !dbg !239
  store i8 %62, i8* %1, align 1, !dbg !239
  br label %34, !dbg !240, !llvm.loop !241

; <label>:63:                                     ; preds = %34
  %64 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2, i32 0, i32 0)), !dbg !243
  ret void, !dbg !244
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #2

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1) #3

; Function Attrs: argmemonly nounwind
declare void @llvm.memset.p0i8.i64(i8* nocapture writeonly, i8, i64, i32, i1) #3

declare i32 @printf(i8*, ...) #1

; Function Attrs: noinline nounwind optnone uwtable
define internal void @phex(i8*) #0 !dbg !245 {
  %2 = alloca i8*, align 8
  %3 = alloca i8, align 1
  store i8* %0, i8** %2, align 8
  call void @llvm.dbg.declare(metadata i8** %2, metadata !249, metadata !DIExpression()), !dbg !250
  call void @llvm.dbg.declare(metadata i8* %3, metadata !251, metadata !DIExpression()), !dbg !252
  store i8 0, i8* %3, align 1, !dbg !253
  br label %4, !dbg !255

; <label>:4:                                      ; preds = %17, %1
  %5 = load i8, i8* %3, align 1, !dbg !256
  %6 = zext i8 %5 to i32, !dbg !256
  %7 = icmp slt i32 %6, 16, !dbg !258
  br i1 %7, label %8, label %20, !dbg !259

; <label>:8:                                      ; preds = %4
  %9 = load i8*, i8** %2, align 8, !dbg !260
  %10 = load i8, i8* %3, align 1, !dbg !262
  %11 = zext i8 %10 to i64, !dbg !260
  %12 = getelementptr inbounds i8, i8* %9, i64 %11, !dbg !260
  %13 = load i8, i8* %12, align 1, !dbg !260
  %14 = zext i8 %13 to i32, !dbg !260
  %15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.5, i32 0, i32 0), i32 %14), !dbg !263
  %16 = call i32 (...) @checkpoint(), !dbg !264
  br label %17, !dbg !265

; <label>:17:                                     ; preds = %8
  %18 = load i8, i8* %3, align 1, !dbg !266
  %19 = add i8 %18, 1, !dbg !266
  store i8 %19, i8* %3, align 1, !dbg !266
  br label %4, !dbg !267, !llvm.loop !268

; <label>:20:                                     ; preds = %4
  %21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2, i32 0, i32 0)), !dbg !270
  ret void, !dbg !271
}

declare void @AES128_ECB_encrypt(i8*, i8*, i8*) #1

; Function Attrs: nounwind readonly
declare i32 @strncmp(i8*, i8*, i64) #4

declare void @AES128_CBC_decrypt_buffer(i8*, i8*, i32, i8*, i8*) #1

declare void @AES128_CBC_encrypt_buffer(i8*, i8*, i32, i8*, i8*) #1

declare void @AES128_ECB_decrypt(i8*, i8*, i8*) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readnone speculatable }
attributes #3 = { argmemonly nounwind }
attributes #4 = { nounwind readonly "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nounwind readonly }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!11, !12, !13}
!llvm.ident = !{!14}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, retainedTypes: !3)
!1 = !DIFile(filename: "main.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/aes_global")
!2 = !{}
!3 = !{!4, !9}
!4 = !DIDerivedType(tag: DW_TAG_typedef, name: "uint8_t", file: !5, line: 24, baseType: !6)
!5 = !DIFile(filename: "/usr/include/x86_64-linux-gnu/bits/stdint-uintn.h", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/aes_global")
!6 = !DIDerivedType(tag: DW_TAG_typedef, name: "__uint8_t", file: !7, line: 38, baseType: !8)
!7 = !DIFile(filename: "/usr/include/x86_64-linux-gnu/bits/types.h", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/aes_global")
!8 = !DIBasicType(name: "unsigned char", size: 8, encoding: DW_ATE_unsigned_char)
!9 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !10, size: 64)
!10 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!11 = !{i32 2, !"Dwarf Version", i32 4}
!12 = !{i32 2, !"Debug Info Version", i32 3}
!13 = !{i32 1, !"wchar_size", i32 4}
!14 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!15 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 22, type: !16, isLocal: false, isDefinition: true, scopeLine: 23, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!16 = !DISubroutineType(types: !17)
!17 = !{!18}
!18 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!19 = !DILocation(line: 25, column: 5, scope: !15)
!20 = !DILocation(line: 26, column: 5, scope: !15)
!21 = !DILocation(line: 28, column: 5, scope: !15)
!22 = !DILocation(line: 29, column: 5, scope: !15)
!23 = !DILocation(line: 31, column: 5, scope: !15)
!24 = !DILocation(line: 32, column: 5, scope: !15)
!25 = !DILocation(line: 34, column: 5, scope: !15)
!26 = !DILocation(line: 35, column: 5, scope: !15)
!27 = !DILocation(line: 37, column: 5, scope: !15)
!28 = !DILocation(line: 38, column: 5, scope: !15)
!29 = !DILocation(line: 40, column: 5, scope: !15)
!30 = distinct !DISubprogram(name: "test_encrypt_cbc", scope: !1, file: !1, line: 168, type: !31, isLocal: true, isDefinition: true, scopeLine: 169, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!31 = !DISubroutineType(types: !32)
!32 = !{null}
!33 = !DILocalVariable(name: "key", scope: !30, file: !1, line: 170, type: !34)
!34 = !DICompositeType(tag: DW_TAG_array_type, baseType: !4, size: 128, elements: !35)
!35 = !{!36}
!36 = !DISubrange(count: 16)
!37 = !DILocation(line: 170, column: 11, scope: !30)
!38 = !DILocalVariable(name: "iv", scope: !30, file: !1, line: 171, type: !34)
!39 = !DILocation(line: 171, column: 11, scope: !30)
!40 = !DILocalVariable(name: "in", scope: !30, file: !1, line: 172, type: !41)
!41 = !DICompositeType(tag: DW_TAG_array_type, baseType: !4, size: 512, elements: !42)
!42 = !{!43}
!43 = !DISubrange(count: 64)
!44 = !DILocation(line: 172, column: 11, scope: !30)
!45 = !DILocalVariable(name: "out", scope: !30, file: !1, line: 176, type: !41)
!46 = !DILocation(line: 176, column: 11, scope: !30)
!47 = !DILocalVariable(name: "buffer", scope: !30, file: !1, line: 180, type: !41)
!48 = !DILocation(line: 180, column: 11, scope: !30)
!49 = !DILocation(line: 182, column: 29, scope: !30)
!50 = !DILocation(line: 182, column: 37, scope: !30)
!51 = !DILocation(line: 182, column: 45, scope: !30)
!52 = !DILocation(line: 182, column: 50, scope: !30)
!53 = !DILocation(line: 182, column: 3, scope: !30)
!54 = !DILocation(line: 183, column: 3, scope: !30)
!55 = !DILocation(line: 185, column: 3, scope: !30)
!56 = !DILocation(line: 187, column: 27, scope: !57)
!57 = distinct !DILexicalBlock(scope: !30, file: !1, line: 187, column: 6)
!58 = !DILocation(line: 187, column: 40, scope: !57)
!59 = !DILocation(line: 187, column: 11, scope: !57)
!60 = !DILocation(line: 187, column: 8, scope: !57)
!61 = !DILocation(line: 187, column: 6, scope: !30)
!62 = !DILocation(line: 190, column: 5, scope: !63)
!63 = distinct !DILexicalBlock(scope: !57, file: !1, line: 188, column: 3)
!64 = !DILocation(line: 191, column: 3, scope: !63)
!65 = !DILocation(line: 195, column: 5, scope: !66)
!66 = distinct !DILexicalBlock(scope: !57, file: !1, line: 193, column: 3)
!67 = !DILocation(line: 197, column: 1, scope: !30)
!68 = distinct !DISubprogram(name: "test_decrypt_cbc", scope: !1, file: !1, line: 126, type: !31, isLocal: true, isDefinition: true, scopeLine: 127, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!69 = !DILocalVariable(name: "key", scope: !68, file: !1, line: 130, type: !34)
!70 = !DILocation(line: 130, column: 11, scope: !68)
!71 = !DILocalVariable(name: "iv", scope: !68, file: !1, line: 131, type: !34)
!72 = !DILocation(line: 131, column: 11, scope: !68)
!73 = !DILocalVariable(name: "in", scope: !68, file: !1, line: 132, type: !41)
!74 = !DILocation(line: 132, column: 11, scope: !68)
!75 = !DILocalVariable(name: "out", scope: !68, file: !1, line: 136, type: !41)
!76 = !DILocation(line: 136, column: 11, scope: !68)
!77 = !DILocalVariable(name: "buffer", scope: !68, file: !1, line: 140, type: !41)
!78 = !DILocation(line: 140, column: 11, scope: !68)
!79 = !DILocation(line: 142, column: 29, scope: !68)
!80 = !DILocation(line: 142, column: 35, scope: !68)
!81 = !DILocation(line: 142, column: 39, scope: !68)
!82 = !DILocation(line: 142, column: 41, scope: !68)
!83 = !DILocation(line: 142, column: 50, scope: !68)
!84 = !DILocation(line: 142, column: 55, scope: !68)
!85 = !DILocation(line: 142, column: 3, scope: !68)
!86 = !DILocation(line: 143, column: 3, scope: !68)
!87 = !DILocation(line: 145, column: 29, scope: !68)
!88 = !DILocation(line: 145, column: 35, scope: !68)
!89 = !DILocation(line: 145, column: 40, scope: !68)
!90 = !DILocation(line: 145, column: 42, scope: !68)
!91 = !DILocation(line: 145, column: 3, scope: !68)
!92 = !DILocation(line: 146, column: 3, scope: !68)
!93 = !DILocation(line: 148, column: 29, scope: !68)
!94 = !DILocation(line: 148, column: 35, scope: !68)
!95 = !DILocation(line: 148, column: 40, scope: !68)
!96 = !DILocation(line: 148, column: 42, scope: !68)
!97 = !DILocation(line: 148, column: 3, scope: !68)
!98 = !DILocation(line: 149, column: 3, scope: !68)
!99 = !DILocation(line: 151, column: 29, scope: !68)
!100 = !DILocation(line: 151, column: 35, scope: !68)
!101 = !DILocation(line: 151, column: 40, scope: !68)
!102 = !DILocation(line: 151, column: 42, scope: !68)
!103 = !DILocation(line: 151, column: 3, scope: !68)
!104 = !DILocation(line: 152, column: 3, scope: !68)
!105 = !DILocation(line: 154, column: 3, scope: !68)
!106 = !DILocation(line: 156, column: 27, scope: !107)
!107 = distinct !DILexicalBlock(scope: !68, file: !1, line: 156, column: 6)
!108 = !DILocation(line: 156, column: 40, scope: !107)
!109 = !DILocation(line: 156, column: 11, scope: !107)
!110 = !DILocation(line: 156, column: 8, scope: !107)
!111 = !DILocation(line: 156, column: 6, scope: !68)
!112 = !DILocation(line: 159, column: 5, scope: !113)
!113 = distinct !DILexicalBlock(scope: !107, file: !1, line: 157, column: 3)
!114 = !DILocation(line: 160, column: 3, scope: !113)
!115 = !DILocation(line: 164, column: 5, scope: !116)
!116 = distinct !DILexicalBlock(scope: !107, file: !1, line: 162, column: 3)
!117 = !DILocation(line: 166, column: 1, scope: !68)
!118 = distinct !DISubprogram(name: "test_decrypt_ecb", scope: !1, file: !1, line: 200, type: !31, isLocal: true, isDefinition: true, scopeLine: 201, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!119 = !DILocalVariable(name: "key", scope: !118, file: !1, line: 202, type: !34)
!120 = !DILocation(line: 202, column: 11, scope: !118)
!121 = !DILocalVariable(name: "in", scope: !118, file: !1, line: 203, type: !34)
!122 = !DILocation(line: 203, column: 11, scope: !118)
!123 = !DILocalVariable(name: "out", scope: !118, file: !1, line: 204, type: !34)
!124 = !DILocation(line: 204, column: 11, scope: !118)
!125 = !DILocalVariable(name: "buffer", scope: !118, file: !1, line: 205, type: !34)
!126 = !DILocation(line: 205, column: 11, scope: !118)
!127 = !DILocation(line: 207, column: 22, scope: !118)
!128 = !DILocation(line: 207, column: 26, scope: !118)
!129 = !DILocation(line: 207, column: 31, scope: !118)
!130 = !DILocation(line: 207, column: 3, scope: !118)
!131 = !DILocation(line: 208, column: 3, scope: !118)
!132 = !DILocation(line: 210, column: 3, scope: !118)
!133 = !DILocation(line: 212, column: 27, scope: !134)
!134 = distinct !DILexicalBlock(scope: !118, file: !1, line: 212, column: 6)
!135 = !DILocation(line: 212, column: 40, scope: !134)
!136 = !DILocation(line: 212, column: 11, scope: !134)
!137 = !DILocation(line: 212, column: 8, scope: !134)
!138 = !DILocation(line: 212, column: 6, scope: !118)
!139 = !DILocation(line: 215, column: 5, scope: !140)
!140 = distinct !DILexicalBlock(scope: !134, file: !1, line: 213, column: 3)
!141 = !DILocation(line: 216, column: 3, scope: !140)
!142 = !DILocation(line: 220, column: 5, scope: !143)
!143 = distinct !DILexicalBlock(scope: !134, file: !1, line: 218, column: 3)
!144 = !DILocation(line: 222, column: 1, scope: !118)
!145 = distinct !DISubprogram(name: "test_encrypt_ecb", scope: !1, file: !1, line: 102, type: !31, isLocal: true, isDefinition: true, scopeLine: 103, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!146 = !DILocalVariable(name: "key", scope: !145, file: !1, line: 104, type: !34)
!147 = !DILocation(line: 104, column: 11, scope: !145)
!148 = !DILocalVariable(name: "in", scope: !145, file: !1, line: 105, type: !34)
!149 = !DILocation(line: 105, column: 11, scope: !145)
!150 = !DILocalVariable(name: "out", scope: !145, file: !1, line: 106, type: !34)
!151 = !DILocation(line: 106, column: 11, scope: !145)
!152 = !DILocalVariable(name: "buffer", scope: !145, file: !1, line: 107, type: !34)
!153 = !DILocation(line: 107, column: 11, scope: !145)
!154 = !DILocation(line: 109, column: 22, scope: !145)
!155 = !DILocation(line: 109, column: 26, scope: !145)
!156 = !DILocation(line: 109, column: 31, scope: !145)
!157 = !DILocation(line: 109, column: 3, scope: !145)
!158 = !DILocation(line: 110, column: 3, scope: !145)
!159 = !DILocation(line: 112, column: 3, scope: !145)
!160 = !DILocation(line: 114, column: 27, scope: !161)
!161 = distinct !DILexicalBlock(scope: !145, file: !1, line: 114, column: 6)
!162 = !DILocation(line: 114, column: 40, scope: !161)
!163 = !DILocation(line: 114, column: 11, scope: !161)
!164 = !DILocation(line: 114, column: 8, scope: !161)
!165 = !DILocation(line: 114, column: 6, scope: !145)
!166 = !DILocation(line: 117, column: 5, scope: !167)
!167 = distinct !DILexicalBlock(scope: !161, file: !1, line: 115, column: 3)
!168 = !DILocation(line: 118, column: 3, scope: !167)
!169 = !DILocation(line: 122, column: 5, scope: !170)
!170 = distinct !DILexicalBlock(scope: !161, file: !1, line: 120, column: 3)
!171 = !DILocation(line: 124, column: 1, scope: !145)
!172 = distinct !DISubprogram(name: "test_encrypt_ecb_verbose", scope: !1, file: !1, line: 56, type: !31, isLocal: true, isDefinition: true, scopeLine: 57, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!173 = !DILocalVariable(name: "i", scope: !172, file: !1, line: 60, type: !4)
!174 = !DILocation(line: 60, column: 13, scope: !172)
!175 = !DILocalVariable(name: "buf", scope: !172, file: !1, line: 60, type: !41)
!176 = !DILocation(line: 60, column: 16, scope: !172)
!177 = !DILocalVariable(name: "buf2", scope: !172, file: !1, line: 60, type: !41)
!178 = !DILocation(line: 60, column: 25, scope: !172)
!179 = !DILocalVariable(name: "key", scope: !172, file: !1, line: 63, type: !34)
!180 = !DILocation(line: 63, column: 13, scope: !172)
!181 = !DILocalVariable(name: "plain_text", scope: !172, file: !1, line: 65, type: !41)
!182 = !DILocation(line: 65, column: 13, scope: !172)
!183 = !DILocation(line: 70, column: 5, scope: !172)
!184 = !DILocation(line: 71, column: 5, scope: !172)
!185 = !DILocation(line: 74, column: 5, scope: !172)
!186 = !DILocation(line: 75, column: 5, scope: !172)
!187 = !DILocation(line: 76, column: 11, scope: !188)
!188 = distinct !DILexicalBlock(scope: !172, file: !1, line: 76, column: 5)
!189 = !DILocation(line: 76, column: 9, scope: !188)
!190 = !DILocation(line: 76, column: 26, scope: !191)
!191 = distinct !DILexicalBlock(scope: !188, file: !1, line: 76, column: 5)
!192 = !DILocation(line: 76, column: 28, scope: !191)
!193 = !DILocation(line: 76, column: 5, scope: !188)
!194 = !DILocation(line: 78, column: 14, scope: !195)
!195 = distinct !DILexicalBlock(scope: !191, file: !1, line: 77, column: 5)
!196 = !DILocation(line: 78, column: 27, scope: !195)
!197 = !DILocation(line: 78, column: 29, scope: !195)
!198 = !DILocation(line: 78, column: 25, scope: !195)
!199 = !DILocation(line: 78, column: 9, scope: !195)
!200 = !DILocation(line: 79, column: 9, scope: !195)
!201 = !DILocation(line: 80, column: 5, scope: !195)
!202 = !DILocation(line: 76, column: 43, scope: !191)
!203 = !DILocation(line: 76, column: 5, scope: !191)
!204 = distinct !{!204, !193, !205}
!205 = !DILocation(line: 80, column: 5, scope: !188)
!206 = !DILocation(line: 81, column: 5, scope: !172)
!207 = !DILocation(line: 83, column: 5, scope: !172)
!208 = !DILocation(line: 84, column: 10, scope: !172)
!209 = !DILocation(line: 84, column: 5, scope: !172)
!210 = !DILocation(line: 85, column: 5, scope: !172)
!211 = !DILocation(line: 87, column: 5, scope: !172)
!212 = !DILocation(line: 90, column: 5, scope: !172)
!213 = !DILocation(line: 91, column: 11, scope: !214)
!214 = distinct !DILexicalBlock(scope: !172, file: !1, line: 91, column: 5)
!215 = !DILocation(line: 91, column: 9, scope: !214)
!216 = !DILocation(line: 91, column: 16, scope: !217)
!217 = distinct !DILexicalBlock(scope: !214, file: !1, line: 91, column: 5)
!218 = !DILocation(line: 91, column: 18, scope: !217)
!219 = !DILocation(line: 91, column: 5, scope: !214)
!220 = !DILocation(line: 93, column: 28, scope: !221)
!221 = distinct !DILexicalBlock(scope: !217, file: !1, line: 92, column: 5)
!222 = !DILocation(line: 93, column: 42, scope: !221)
!223 = !DILocation(line: 93, column: 43, scope: !221)
!224 = !DILocation(line: 93, column: 39, scope: !221)
!225 = !DILocation(line: 93, column: 49, scope: !221)
!226 = !DILocation(line: 93, column: 54, scope: !221)
!227 = !DILocation(line: 93, column: 59, scope: !221)
!228 = !DILocation(line: 93, column: 60, scope: !221)
!229 = !DILocation(line: 93, column: 57, scope: !221)
!230 = !DILocation(line: 93, column: 9, scope: !221)
!231 = !DILocation(line: 94, column: 9, scope: !221)
!232 = !DILocation(line: 95, column: 14, scope: !221)
!233 = !DILocation(line: 95, column: 21, scope: !221)
!234 = !DILocation(line: 95, column: 22, scope: !221)
!235 = !DILocation(line: 95, column: 18, scope: !221)
!236 = !DILocation(line: 95, column: 9, scope: !221)
!237 = !DILocation(line: 96, column: 9, scope: !221)
!238 = !DILocation(line: 97, column: 5, scope: !221)
!239 = !DILocation(line: 91, column: 23, scope: !217)
!240 = !DILocation(line: 91, column: 5, scope: !217)
!241 = distinct !{!241, !219, !242}
!242 = !DILocation(line: 97, column: 5, scope: !214)
!243 = !DILocation(line: 98, column: 5, scope: !172)
!244 = !DILocation(line: 99, column: 1, scope: !172)
!245 = distinct !DISubprogram(name: "phex", scope: !1, file: !1, line: 46, type: !246, isLocal: true, isDefinition: true, scopeLine: 47, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!246 = !DISubroutineType(types: !247)
!247 = !{null, !248}
!248 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !4, size: 64)
!249 = !DILocalVariable(name: "str", arg: 1, scope: !245, file: !1, line: 46, type: !248)
!250 = !DILocation(line: 46, column: 27, scope: !245)
!251 = !DILocalVariable(name: "i", scope: !245, file: !1, line: 48, type: !8)
!252 = !DILocation(line: 48, column: 19, scope: !245)
!253 = !DILocation(line: 49, column: 11, scope: !254)
!254 = distinct !DILexicalBlock(scope: !245, file: !1, line: 49, column: 5)
!255 = !DILocation(line: 49, column: 9, scope: !254)
!256 = !DILocation(line: 49, column: 16, scope: !257)
!257 = distinct !DILexicalBlock(scope: !254, file: !1, line: 49, column: 5)
!258 = !DILocation(line: 49, column: 18, scope: !257)
!259 = !DILocation(line: 49, column: 5, scope: !254)
!260 = !DILocation(line: 50, column: 24, scope: !261)
!261 = distinct !DILexicalBlock(scope: !257, file: !1, line: 49, column: 29)
!262 = !DILocation(line: 50, column: 28, scope: !261)
!263 = !DILocation(line: 50, column: 9, scope: !261)
!264 = !DILocation(line: 51, column: 9, scope: !261)
!265 = !DILocation(line: 52, column: 7, scope: !261)
!266 = !DILocation(line: 49, column: 24, scope: !257)
!267 = !DILocation(line: 49, column: 5, scope: !257)
!268 = distinct !{!268, !259, !269}
!269 = !DILocation(line: 52, column: 7, scope: !254)
!270 = !DILocation(line: 53, column: 5, scope: !245)
!271 = !DILocation(line: 54, column: 1, scope: !245)
