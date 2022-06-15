; ModuleID = 'crc.c'
source_filename = "crc.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@crcTable = common global [256 x i16] zeroinitializer, align 16, !dbg !0

; Function Attrs: noinline nounwind optnone uwtable
define zeroext i16 @crcSlow(i8*, i32) #0 !dbg !16 {
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i16, align 2
  %6 = alloca i32, align 4
  %7 = alloca i8, align 1
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !23, metadata !DIExpression()), !dbg !24
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !25, metadata !DIExpression()), !dbg !26
  call void @llvm.dbg.declare(metadata i16* %5, metadata !27, metadata !DIExpression()), !dbg !28
  store i16 -1, i16* %5, align 2, !dbg !28
  call void @llvm.dbg.declare(metadata i32* %6, metadata !29, metadata !DIExpression()), !dbg !30
  call void @llvm.dbg.declare(metadata i8* %7, metadata !31, metadata !DIExpression()), !dbg !32
  store i32 0, i32* %6, align 4, !dbg !33
  br label %8, !dbg !35

; <label>:8:                                      ; preds = %51, %2
  %9 = load i32, i32* %6, align 4, !dbg !36
  %10 = load i32, i32* %4, align 4, !dbg !38
  %11 = icmp slt i32 %9, %10, !dbg !39
  br i1 %11, label %12, label %54, !dbg !40

; <label>:12:                                     ; preds = %8
  %13 = load i8*, i8** %3, align 8, !dbg !41
  %14 = load i32, i32* %6, align 4, !dbg !41
  %15 = sext i32 %14 to i64, !dbg !41
  %16 = getelementptr inbounds i8, i8* %13, i64 %15, !dbg !41
  %17 = load i8, i8* %16, align 1, !dbg !41
  %18 = zext i8 %17 to i32, !dbg !41
  %19 = shl i32 %18, 8, !dbg !43
  %20 = load i16, i16* %5, align 2, !dbg !44
  %21 = zext i16 %20 to i32, !dbg !44
  %22 = xor i32 %21, %19, !dbg !44
  %23 = trunc i32 %22 to i16, !dbg !44
  store i16 %23, i16* %5, align 2, !dbg !44
  store i8 8, i8* %7, align 1, !dbg !45
  br label %24, !dbg !47

; <label>:24:                                     ; preds = %46, %12
  %25 = load i8, i8* %7, align 1, !dbg !48
  %26 = zext i8 %25 to i32, !dbg !48
  %27 = icmp sgt i32 %26, 0, !dbg !50
  br i1 %27, label %28, label %49, !dbg !51

; <label>:28:                                     ; preds = %24
  %29 = load i16, i16* %5, align 2, !dbg !52
  %30 = zext i16 %29 to i32, !dbg !52
  %31 = and i32 %30, 32768, !dbg !55
  %32 = icmp ne i32 %31, 0, !dbg !55
  br i1 %32, label %33, label %39, !dbg !56

; <label>:33:                                     ; preds = %28
  %34 = load i16, i16* %5, align 2, !dbg !57
  %35 = zext i16 %34 to i32, !dbg !57
  %36 = shl i32 %35, 1, !dbg !59
  %37 = xor i32 %36, 4129, !dbg !60
  %38 = trunc i32 %37 to i16, !dbg !61
  store i16 %38, i16* %5, align 2, !dbg !62
  br label %44, !dbg !63

; <label>:39:                                     ; preds = %28
  %40 = load i16, i16* %5, align 2, !dbg !64
  %41 = zext i16 %40 to i32, !dbg !64
  %42 = shl i32 %41, 1, !dbg !66
  %43 = trunc i32 %42 to i16, !dbg !67
  store i16 %43, i16* %5, align 2, !dbg !68
  br label %44

; <label>:44:                                     ; preds = %39, %33
  %45 = call i32 (...) @checkpoint(), !dbg !69
  br label %46, !dbg !70

; <label>:46:                                     ; preds = %44
  %47 = load i8, i8* %7, align 1, !dbg !71
  %48 = add i8 %47, -1, !dbg !71
  store i8 %48, i8* %7, align 1, !dbg !71
  br label %24, !dbg !72, !llvm.loop !73

; <label>:49:                                     ; preds = %24
  %50 = call i32 (...) @checkpoint(), !dbg !75
  br label %51, !dbg !76

; <label>:51:                                     ; preds = %49
  %52 = load i32, i32* %6, align 4, !dbg !77
  %53 = add nsw i32 %52, 1, !dbg !77
  store i32 %53, i32* %6, align 4, !dbg !77
  br label %8, !dbg !78, !llvm.loop !79

; <label>:54:                                     ; preds = %8
  %55 = load i16, i16* %5, align 2, !dbg !81
  %56 = zext i16 %55 to i32, !dbg !81
  %57 = xor i32 %56, 0, !dbg !82
  %58 = trunc i32 %57 to i16, !dbg !83
  ret i16 %58, !dbg !84
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

declare i32 @checkpoint(...) #2

; Function Attrs: noinline nounwind optnone uwtable
define void @crcInit() #0 !dbg !85 {
  %1 = alloca i16, align 2
  %2 = alloca i32, align 4
  %3 = alloca i8, align 1
  call void @llvm.dbg.declare(metadata i16* %1, metadata !88, metadata !DIExpression()), !dbg !89
  call void @llvm.dbg.declare(metadata i32* %2, metadata !90, metadata !DIExpression()), !dbg !91
  call void @llvm.dbg.declare(metadata i8* %3, metadata !92, metadata !DIExpression()), !dbg !93
  store i32 0, i32* %2, align 4, !dbg !94
  br label %4, !dbg !96

; <label>:4:                                      ; preds = %42, %0
  %5 = load i32, i32* %2, align 4, !dbg !97
  %6 = icmp slt i32 %5, 256, !dbg !99
  br i1 %6, label %7, label %45, !dbg !100

; <label>:7:                                      ; preds = %4
  %8 = load i32, i32* %2, align 4, !dbg !101
  %9 = shl i32 %8, 8, !dbg !103
  %10 = trunc i32 %9 to i16, !dbg !101
  store i16 %10, i16* %1, align 2, !dbg !104
  store i8 8, i8* %3, align 1, !dbg !105
  br label %11, !dbg !107

; <label>:11:                                     ; preds = %33, %7
  %12 = load i8, i8* %3, align 1, !dbg !108
  %13 = zext i8 %12 to i32, !dbg !108
  %14 = icmp sgt i32 %13, 0, !dbg !110
  br i1 %14, label %15, label %36, !dbg !111

; <label>:15:                                     ; preds = %11
  %16 = load i16, i16* %1, align 2, !dbg !112
  %17 = zext i16 %16 to i32, !dbg !112
  %18 = and i32 %17, 32768, !dbg !115
  %19 = icmp ne i32 %18, 0, !dbg !115
  br i1 %19, label %20, label %26, !dbg !116

; <label>:20:                                     ; preds = %15
  %21 = load i16, i16* %1, align 2, !dbg !117
  %22 = zext i16 %21 to i32, !dbg !117
  %23 = shl i32 %22, 1, !dbg !119
  %24 = xor i32 %23, 4129, !dbg !120
  %25 = trunc i32 %24 to i16, !dbg !121
  store i16 %25, i16* %1, align 2, !dbg !122
  br label %31, !dbg !123

; <label>:26:                                     ; preds = %15
  %27 = load i16, i16* %1, align 2, !dbg !124
  %28 = zext i16 %27 to i32, !dbg !124
  %29 = shl i32 %28, 1, !dbg !126
  %30 = trunc i32 %29 to i16, !dbg !127
  store i16 %30, i16* %1, align 2, !dbg !128
  br label %31

; <label>:31:                                     ; preds = %26, %20
  %32 = call i32 (...) @checkpoint(), !dbg !129
  br label %33, !dbg !130

; <label>:33:                                     ; preds = %31
  %34 = load i8, i8* %3, align 1, !dbg !131
  %35 = add i8 %34, -1, !dbg !131
  store i8 %35, i8* %3, align 1, !dbg !131
  br label %11, !dbg !132, !llvm.loop !133

; <label>:36:                                     ; preds = %11
  %37 = load i16, i16* %1, align 2, !dbg !135
  %38 = load i32, i32* %2, align 4, !dbg !136
  %39 = sext i32 %38 to i64, !dbg !137
  %40 = getelementptr inbounds [256 x i16], [256 x i16]* @crcTable, i64 0, i64 %39, !dbg !137
  store i16 %37, i16* %40, align 2, !dbg !138
  %41 = call i32 (...) @checkpoint(), !dbg !139
  br label %42, !dbg !140

; <label>:42:                                     ; preds = %36
  %43 = load i32, i32* %2, align 4, !dbg !141
  %44 = add nsw i32 %43, 1, !dbg !141
  store i32 %44, i32* %2, align 4, !dbg !141
  br label %4, !dbg !142, !llvm.loop !143

; <label>:45:                                     ; preds = %4
  ret void, !dbg !145
}

; Function Attrs: noinline nounwind optnone uwtable
define zeroext i16 @crcFast(i8*, i32) #0 !dbg !146 {
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i16, align 2
  %6 = alloca i8, align 1
  %7 = alloca i32, align 4
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !147, metadata !DIExpression()), !dbg !148
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !149, metadata !DIExpression()), !dbg !150
  call void @llvm.dbg.declare(metadata i16* %5, metadata !151, metadata !DIExpression()), !dbg !152
  store i16 -1, i16* %5, align 2, !dbg !152
  call void @llvm.dbg.declare(metadata i8* %6, metadata !153, metadata !DIExpression()), !dbg !154
  call void @llvm.dbg.declare(metadata i32* %7, metadata !155, metadata !DIExpression()), !dbg !156
  store i32 0, i32* %7, align 4, !dbg !157
  br label %8, !dbg !159

; <label>:8:                                      ; preds = %35, %2
  %9 = load i32, i32* %7, align 4, !dbg !160
  %10 = load i32, i32* %4, align 4, !dbg !162
  %11 = icmp slt i32 %9, %10, !dbg !163
  br i1 %11, label %12, label %38, !dbg !164

; <label>:12:                                     ; preds = %8
  %13 = load i8*, i8** %3, align 8, !dbg !165
  %14 = load i32, i32* %7, align 4, !dbg !165
  %15 = sext i32 %14 to i64, !dbg !165
  %16 = getelementptr inbounds i8, i8* %13, i64 %15, !dbg !165
  %17 = load i8, i8* %16, align 1, !dbg !165
  %18 = zext i8 %17 to i32, !dbg !165
  %19 = load i16, i16* %5, align 2, !dbg !167
  %20 = zext i16 %19 to i32, !dbg !167
  %21 = ashr i32 %20, 8, !dbg !168
  %22 = xor i32 %18, %21, !dbg !169
  %23 = trunc i32 %22 to i8, !dbg !165
  store i8 %23, i8* %6, align 1, !dbg !170
  %24 = load i8, i8* %6, align 1, !dbg !171
  %25 = zext i8 %24 to i64, !dbg !172
  %26 = getelementptr inbounds [256 x i16], [256 x i16]* @crcTable, i64 0, i64 %25, !dbg !172
  %27 = load i16, i16* %26, align 2, !dbg !172
  %28 = zext i16 %27 to i32, !dbg !172
  %29 = load i16, i16* %5, align 2, !dbg !173
  %30 = zext i16 %29 to i32, !dbg !173
  %31 = shl i32 %30, 8, !dbg !174
  %32 = xor i32 %28, %31, !dbg !175
  %33 = trunc i32 %32 to i16, !dbg !172
  store i16 %33, i16* %5, align 2, !dbg !176
  %34 = call i32 (...) @checkpoint(), !dbg !177
  br label %35, !dbg !178

; <label>:35:                                     ; preds = %12
  %36 = load i32, i32* %7, align 4, !dbg !179
  %37 = add nsw i32 %36, 1, !dbg !179
  store i32 %37, i32* %7, align 4, !dbg !179
  br label %8, !dbg !180, !llvm.loop !181

; <label>:38:                                     ; preds = %8
  %39 = load i16, i16* %5, align 2, !dbg !183
  %40 = zext i16 %39 to i32, !dbg !183
  %41 = xor i32 %40, 0, !dbg !184
  %42 = trunc i32 %41 to i16, !dbg !185
  ret i16 %42, !dbg !186
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!12, !13, !14}
!llvm.ident = !{!15}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "crcTable", scope: !2, file: !3, line: 143, type: !6, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5)
!3 = !DIFile(filename: "crc.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_global_mini")
!4 = !{}
!5 = !{!0}
!6 = !DICompositeType(tag: DW_TAG_array_type, baseType: !7, size: 4096, elements: !10)
!7 = !DIDerivedType(tag: DW_TAG_typedef, name: "crc", file: !8, line: 31, baseType: !9)
!8 = !DIFile(filename: "./crc.h", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_global_mini")
!9 = !DIBasicType(name: "unsigned short", size: 16, encoding: DW_ATE_unsigned)
!10 = !{!11}
!11 = !DISubrange(count: 256)
!12 = !{i32 2, !"Dwarf Version", i32 4}
!13 = !{i32 2, !"Debug Info Version", i32 3}
!14 = !{i32 1, !"wchar_size", i32 4}
!15 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!16 = distinct !DISubprogram(name: "crcSlow", scope: !3, file: !3, line: 97, type: !17, isLocal: false, isDefinition: true, scopeLine: 98, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!17 = !DISubroutineType(types: !18)
!18 = !{!7, !19, !22}
!19 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !20, size: 64)
!20 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !21)
!21 = !DIBasicType(name: "unsigned char", size: 8, encoding: DW_ATE_unsigned_char)
!22 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!23 = !DILocalVariable(name: "message", arg: 1, scope: !16, file: !3, line: 97, type: !19)
!24 = !DILocation(line: 97, column: 29, scope: !16)
!25 = !DILocalVariable(name: "nBytes", arg: 2, scope: !16, file: !3, line: 97, type: !22)
!26 = !DILocation(line: 97, column: 44, scope: !16)
!27 = !DILocalVariable(name: "remainder", scope: !16, file: !3, line: 99, type: !7)
!28 = !DILocation(line: 99, column: 20, scope: !16)
!29 = !DILocalVariable(name: "byte", scope: !16, file: !3, line: 100, type: !22)
!30 = !DILocation(line: 100, column: 17, scope: !16)
!31 = !DILocalVariable(name: "bit", scope: !16, file: !3, line: 101, type: !21)
!32 = !DILocation(line: 101, column: 17, scope: !16)
!33 = !DILocation(line: 107, column: 15, scope: !34)
!34 = distinct !DILexicalBlock(scope: !16, file: !3, line: 107, column: 5)
!35 = !DILocation(line: 107, column: 10, scope: !34)
!36 = !DILocation(line: 107, column: 20, scope: !37)
!37 = distinct !DILexicalBlock(scope: !34, file: !3, line: 107, column: 5)
!38 = !DILocation(line: 107, column: 27, scope: !37)
!39 = !DILocation(line: 107, column: 25, scope: !37)
!40 = !DILocation(line: 107, column: 5, scope: !34)
!41 = !DILocation(line: 112, column: 23, scope: !42)
!42 = distinct !DILexicalBlock(scope: !37, file: !3, line: 108, column: 5)
!43 = !DILocation(line: 112, column: 51, scope: !42)
!44 = !DILocation(line: 112, column: 19, scope: !42)
!45 = !DILocation(line: 117, column: 18, scope: !46)
!46 = distinct !DILexicalBlock(scope: !42, file: !3, line: 117, column: 9)
!47 = !DILocation(line: 117, column: 14, scope: !46)
!48 = !DILocation(line: 117, column: 23, scope: !49)
!49 = distinct !DILexicalBlock(scope: !46, file: !3, line: 117, column: 9)
!50 = !DILocation(line: 117, column: 27, scope: !49)
!51 = !DILocation(line: 117, column: 9, scope: !46)
!52 = !DILocation(line: 122, column: 17, scope: !53)
!53 = distinct !DILexicalBlock(scope: !54, file: !3, line: 122, column: 17)
!54 = distinct !DILexicalBlock(scope: !49, file: !3, line: 118, column: 9)
!55 = !DILocation(line: 122, column: 27, scope: !53)
!56 = !DILocation(line: 122, column: 17, scope: !54)
!57 = !DILocation(line: 124, column: 30, scope: !58)
!58 = distinct !DILexicalBlock(scope: !53, file: !3, line: 123, column: 13)
!59 = !DILocation(line: 124, column: 40, scope: !58)
!60 = !DILocation(line: 124, column: 46, scope: !58)
!61 = !DILocation(line: 124, column: 29, scope: !58)
!62 = !DILocation(line: 124, column: 27, scope: !58)
!63 = !DILocation(line: 125, column: 13, scope: !58)
!64 = !DILocation(line: 128, column: 30, scope: !65)
!65 = distinct !DILexicalBlock(scope: !53, file: !3, line: 127, column: 13)
!66 = !DILocation(line: 128, column: 40, scope: !65)
!67 = !DILocation(line: 128, column: 29, scope: !65)
!68 = !DILocation(line: 128, column: 27, scope: !65)
!69 = !DILocation(line: 130, column: 13, scope: !54)
!70 = !DILocation(line: 131, column: 9, scope: !54)
!71 = !DILocation(line: 117, column: 32, scope: !49)
!72 = !DILocation(line: 117, column: 9, scope: !49)
!73 = distinct !{!73, !51, !74}
!74 = !DILocation(line: 131, column: 9, scope: !46)
!75 = !DILocation(line: 132, column: 9, scope: !42)
!76 = !DILocation(line: 133, column: 5, scope: !42)
!77 = !DILocation(line: 107, column: 35, scope: !37)
!78 = !DILocation(line: 107, column: 5, scope: !37)
!79 = distinct !{!79, !40, !80}
!80 = !DILocation(line: 133, column: 5, scope: !34)
!81 = !DILocation(line: 138, column: 13, scope: !16)
!82 = !DILocation(line: 138, column: 42, scope: !16)
!83 = !DILocation(line: 138, column: 12, scope: !16)
!84 = !DILocation(line: 138, column: 5, scope: !16)
!85 = distinct !DISubprogram(name: "crcInit", scope: !3, file: !3, line: 160, type: !86, isLocal: false, isDefinition: true, scopeLine: 161, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!86 = !DISubroutineType(types: !87)
!87 = !{null}
!88 = !DILocalVariable(name: "remainder", scope: !85, file: !3, line: 162, type: !7)
!89 = !DILocation(line: 162, column: 14, scope: !85)
!90 = !DILocalVariable(name: "dividend", scope: !85, file: !3, line: 163, type: !22)
!91 = !DILocation(line: 163, column: 11, scope: !85)
!92 = !DILocalVariable(name: "bit", scope: !85, file: !3, line: 164, type: !21)
!93 = !DILocation(line: 164, column: 17, scope: !85)
!94 = !DILocation(line: 170, column: 19, scope: !95)
!95 = distinct !DILexicalBlock(scope: !85, file: !3, line: 170, column: 5)
!96 = !DILocation(line: 170, column: 10, scope: !95)
!97 = !DILocation(line: 170, column: 24, scope: !98)
!98 = distinct !DILexicalBlock(scope: !95, file: !3, line: 170, column: 5)
!99 = !DILocation(line: 170, column: 33, scope: !98)
!100 = !DILocation(line: 170, column: 5, scope: !95)
!101 = !DILocation(line: 175, column: 21, scope: !102)
!102 = distinct !DILexicalBlock(scope: !98, file: !3, line: 171, column: 5)
!103 = !DILocation(line: 175, column: 30, scope: !102)
!104 = !DILocation(line: 175, column: 19, scope: !102)
!105 = !DILocation(line: 180, column: 18, scope: !106)
!106 = distinct !DILexicalBlock(scope: !102, file: !3, line: 180, column: 9)
!107 = !DILocation(line: 180, column: 14, scope: !106)
!108 = !DILocation(line: 180, column: 23, scope: !109)
!109 = distinct !DILexicalBlock(scope: !106, file: !3, line: 180, column: 9)
!110 = !DILocation(line: 180, column: 27, scope: !109)
!111 = !DILocation(line: 180, column: 9, scope: !106)
!112 = !DILocation(line: 185, column: 17, scope: !113)
!113 = distinct !DILexicalBlock(scope: !114, file: !3, line: 185, column: 17)
!114 = distinct !DILexicalBlock(scope: !109, file: !3, line: 181, column: 9)
!115 = !DILocation(line: 185, column: 27, scope: !113)
!116 = !DILocation(line: 185, column: 17, scope: !114)
!117 = !DILocation(line: 187, column: 30, scope: !118)
!118 = distinct !DILexicalBlock(scope: !113, file: !3, line: 186, column: 13)
!119 = !DILocation(line: 187, column: 40, scope: !118)
!120 = !DILocation(line: 187, column: 46, scope: !118)
!121 = !DILocation(line: 187, column: 29, scope: !118)
!122 = !DILocation(line: 187, column: 27, scope: !118)
!123 = !DILocation(line: 188, column: 13, scope: !118)
!124 = !DILocation(line: 191, column: 30, scope: !125)
!125 = distinct !DILexicalBlock(scope: !113, file: !3, line: 190, column: 13)
!126 = !DILocation(line: 191, column: 40, scope: !125)
!127 = !DILocation(line: 191, column: 29, scope: !125)
!128 = !DILocation(line: 191, column: 27, scope: !125)
!129 = !DILocation(line: 193, column: 13, scope: !114)
!130 = !DILocation(line: 194, column: 9, scope: !114)
!131 = !DILocation(line: 180, column: 32, scope: !109)
!132 = !DILocation(line: 180, column: 9, scope: !109)
!133 = distinct !{!133, !111, !134}
!134 = !DILocation(line: 194, column: 9, scope: !106)
!135 = !DILocation(line: 199, column: 30, scope: !102)
!136 = !DILocation(line: 199, column: 18, scope: !102)
!137 = !DILocation(line: 199, column: 9, scope: !102)
!138 = !DILocation(line: 199, column: 28, scope: !102)
!139 = !DILocation(line: 200, column: 9, scope: !102)
!140 = !DILocation(line: 201, column: 5, scope: !102)
!141 = !DILocation(line: 170, column: 40, scope: !98)
!142 = !DILocation(line: 170, column: 5, scope: !98)
!143 = distinct !{!143, !100, !144}
!144 = !DILocation(line: 201, column: 5, scope: !95)
!145 = !DILocation(line: 203, column: 1, scope: !85)
!146 = distinct !DISubprogram(name: "crcFast", scope: !3, file: !3, line: 218, type: !17, isLocal: false, isDefinition: true, scopeLine: 219, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!147 = !DILocalVariable(name: "message", arg: 1, scope: !146, file: !3, line: 218, type: !19)
!148 = !DILocation(line: 218, column: 29, scope: !146)
!149 = !DILocalVariable(name: "nBytes", arg: 2, scope: !146, file: !3, line: 218, type: !22)
!150 = !DILocation(line: 218, column: 44, scope: !146)
!151 = !DILocalVariable(name: "remainder", scope: !146, file: !3, line: 220, type: !7)
!152 = !DILocation(line: 220, column: 20, scope: !146)
!153 = !DILocalVariable(name: "data", scope: !146, file: !3, line: 221, type: !21)
!154 = !DILocation(line: 221, column: 20, scope: !146)
!155 = !DILocalVariable(name: "byte", scope: !146, file: !3, line: 222, type: !22)
!156 = !DILocation(line: 222, column: 17, scope: !146)
!157 = !DILocation(line: 228, column: 15, scope: !158)
!158 = distinct !DILexicalBlock(scope: !146, file: !3, line: 228, column: 5)
!159 = !DILocation(line: 228, column: 10, scope: !158)
!160 = !DILocation(line: 228, column: 20, scope: !161)
!161 = distinct !DILexicalBlock(scope: !158, file: !3, line: 228, column: 5)
!162 = !DILocation(line: 228, column: 27, scope: !161)
!163 = !DILocation(line: 228, column: 25, scope: !161)
!164 = !DILocation(line: 228, column: 5, scope: !158)
!165 = !DILocation(line: 230, column: 16, scope: !166)
!166 = distinct !DILexicalBlock(scope: !161, file: !3, line: 229, column: 5)
!167 = !DILocation(line: 230, column: 47, scope: !166)
!168 = !DILocation(line: 230, column: 57, scope: !166)
!169 = !DILocation(line: 230, column: 44, scope: !166)
!170 = !DILocation(line: 230, column: 14, scope: !166)
!171 = !DILocation(line: 231, column: 26, scope: !166)
!172 = !DILocation(line: 231, column: 17, scope: !166)
!173 = !DILocation(line: 231, column: 35, scope: !166)
!174 = !DILocation(line: 231, column: 45, scope: !166)
!175 = !DILocation(line: 231, column: 32, scope: !166)
!176 = !DILocation(line: 231, column: 15, scope: !166)
!177 = !DILocation(line: 232, column: 7, scope: !166)
!178 = !DILocation(line: 233, column: 5, scope: !166)
!179 = !DILocation(line: 228, column: 35, scope: !161)
!180 = !DILocation(line: 228, column: 5, scope: !161)
!181 = distinct !{!181, !164, !182}
!182 = !DILocation(line: 233, column: 5, scope: !158)
!183 = !DILocation(line: 238, column: 13, scope: !146)
!184 = !DILocation(line: 238, column: 42, scope: !146)
!185 = !DILocation(line: 238, column: 12, scope: !146)
!186 = !DILocation(line: 238, column: 5, scope: !146)
