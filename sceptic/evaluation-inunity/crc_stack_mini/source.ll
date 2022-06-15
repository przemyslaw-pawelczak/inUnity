; ModuleID = 'llvm-link'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@main.test = private unnamed_addr constant [10 x i8] c"123456789\00", align 1
@crcTable = common global [256 x i16] zeroinitializer, align 16, !dbg !0

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 !dbg !18 {
  %1 = alloca i32, align 4
  %2 = alloca [10 x i8], align 1
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata [10 x i8]* %2, metadata !22, metadata !DIExpression()), !dbg !27
  %3 = bitcast [10 x i8]* %2 to i8*, !dbg !27
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %3, i8* getelementptr inbounds ([10 x i8], [10 x i8]* @main.test, i32 0, i32 0), i64 10, i32 1, i1 false), !dbg !27
  %4 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !28
  %5 = call zeroext i16 @crcSlow(i8* %4, i32 9), !dbg !29
  ret i32 0, !dbg !30
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1) #2

; Function Attrs: noinline nounwind optnone uwtable
define zeroext i16 @crcSlow(i8*, i32) #0 !dbg !31 {
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i16, align 2
  %6 = alloca i32, align 4
  %7 = alloca i8, align 1
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !36, metadata !DIExpression()), !dbg !37
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !38, metadata !DIExpression()), !dbg !39
  call void @llvm.dbg.declare(metadata i16* %5, metadata !40, metadata !DIExpression()), !dbg !41
  store i16 -1, i16* %5, align 2, !dbg !41
  call void @llvm.dbg.declare(metadata i32* %6, metadata !42, metadata !DIExpression()), !dbg !43
  call void @llvm.dbg.declare(metadata i8* %7, metadata !44, metadata !DIExpression()), !dbg !45
  store i32 0, i32* %6, align 4, !dbg !46
  br label %8, !dbg !48

; <label>:8:                                      ; preds = %51, %2
  %9 = load i32, i32* %6, align 4, !dbg !49
  %10 = load i32, i32* %4, align 4, !dbg !51
  %11 = icmp slt i32 %9, %10, !dbg !52
  br i1 %11, label %12, label %54, !dbg !53

; <label>:12:                                     ; preds = %8
  %13 = load i8*, i8** %3, align 8, !dbg !54
  %14 = load i32, i32* %6, align 4, !dbg !54
  %15 = sext i32 %14 to i64, !dbg !54
  %16 = getelementptr inbounds i8, i8* %13, i64 %15, !dbg !54
  %17 = load i8, i8* %16, align 1, !dbg !54
  %18 = zext i8 %17 to i32, !dbg !54
  %19 = shl i32 %18, 8, !dbg !56
  %20 = load i16, i16* %5, align 2, !dbg !57
  %21 = zext i16 %20 to i32, !dbg !57
  %22 = xor i32 %21, %19, !dbg !57
  %23 = trunc i32 %22 to i16, !dbg !57
  store i16 %23, i16* %5, align 2, !dbg !57
  store i8 8, i8* %7, align 1, !dbg !58
  br label %24, !dbg !60

; <label>:24:                                     ; preds = %46, %12
  %25 = load i8, i8* %7, align 1, !dbg !61
  %26 = zext i8 %25 to i32, !dbg !61
  %27 = icmp sgt i32 %26, 0, !dbg !63
  br i1 %27, label %28, label %49, !dbg !64

; <label>:28:                                     ; preds = %24
  %29 = load i16, i16* %5, align 2, !dbg !65
  %30 = zext i16 %29 to i32, !dbg !65
  %31 = and i32 %30, 32768, !dbg !68
  %32 = icmp ne i32 %31, 0, !dbg !68
  br i1 %32, label %33, label %39, !dbg !69

; <label>:33:                                     ; preds = %28
  %34 = load i16, i16* %5, align 2, !dbg !70
  %35 = zext i16 %34 to i32, !dbg !70
  %36 = shl i32 %35, 1, !dbg !72
  %37 = xor i32 %36, 4129, !dbg !73
  %38 = trunc i32 %37 to i16, !dbg !74
  store i16 %38, i16* %5, align 2, !dbg !75
  br label %44, !dbg !76

; <label>:39:                                     ; preds = %28
  %40 = load i16, i16* %5, align 2, !dbg !77
  %41 = zext i16 %40 to i32, !dbg !77
  %42 = shl i32 %41, 1, !dbg !79
  %43 = trunc i32 %42 to i16, !dbg !80
  store i16 %43, i16* %5, align 2, !dbg !81
  br label %44

; <label>:44:                                     ; preds = %39, %33
  %45 = call i32 (...) @checkpoint(), !dbg !82
  br label %46, !dbg !83

; <label>:46:                                     ; preds = %44
  %47 = load i8, i8* %7, align 1, !dbg !84
  %48 = add i8 %47, -1, !dbg !84
  store i8 %48, i8* %7, align 1, !dbg !84
  br label %24, !dbg !85, !llvm.loop !86

; <label>:49:                                     ; preds = %24
  %50 = call i32 (...) @checkpoint(), !dbg !88
  br label %51, !dbg !89

; <label>:51:                                     ; preds = %49
  %52 = load i32, i32* %6, align 4, !dbg !90
  %53 = add nsw i32 %52, 1, !dbg !90
  store i32 %53, i32* %6, align 4, !dbg !90
  br label %8, !dbg !91, !llvm.loop !92

; <label>:54:                                     ; preds = %8
  %55 = load i16, i16* %5, align 2, !dbg !94
  %56 = zext i16 %55 to i32, !dbg !94
  %57 = xor i32 %56, 0, !dbg !95
  %58 = trunc i32 %57 to i16, !dbg !96
  ret i16 %58, !dbg !97
}

declare i32 @checkpoint(...) #3

; Function Attrs: noinline nounwind optnone uwtable
define void @crcInit() #0 !dbg !98 {
  %1 = alloca i16, align 2
  %2 = alloca i32, align 4
  %3 = alloca i8, align 1
  call void @llvm.dbg.declare(metadata i16* %1, metadata !101, metadata !DIExpression()), !dbg !102
  call void @llvm.dbg.declare(metadata i32* %2, metadata !103, metadata !DIExpression()), !dbg !104
  call void @llvm.dbg.declare(metadata i8* %3, metadata !105, metadata !DIExpression()), !dbg !106
  store i32 0, i32* %2, align 4, !dbg !107
  br label %4, !dbg !109

; <label>:4:                                      ; preds = %42, %0
  %5 = load i32, i32* %2, align 4, !dbg !110
  %6 = icmp slt i32 %5, 256, !dbg !112
  br i1 %6, label %7, label %45, !dbg !113

; <label>:7:                                      ; preds = %4
  %8 = load i32, i32* %2, align 4, !dbg !114
  %9 = shl i32 %8, 8, !dbg !116
  %10 = trunc i32 %9 to i16, !dbg !114
  store i16 %10, i16* %1, align 2, !dbg !117
  store i8 8, i8* %3, align 1, !dbg !118
  br label %11, !dbg !120

; <label>:11:                                     ; preds = %33, %7
  %12 = load i8, i8* %3, align 1, !dbg !121
  %13 = zext i8 %12 to i32, !dbg !121
  %14 = icmp sgt i32 %13, 0, !dbg !123
  br i1 %14, label %15, label %36, !dbg !124

; <label>:15:                                     ; preds = %11
  %16 = load i16, i16* %1, align 2, !dbg !125
  %17 = zext i16 %16 to i32, !dbg !125
  %18 = and i32 %17, 32768, !dbg !128
  %19 = icmp ne i32 %18, 0, !dbg !128
  br i1 %19, label %20, label %26, !dbg !129

; <label>:20:                                     ; preds = %15
  %21 = load i16, i16* %1, align 2, !dbg !130
  %22 = zext i16 %21 to i32, !dbg !130
  %23 = shl i32 %22, 1, !dbg !132
  %24 = xor i32 %23, 4129, !dbg !133
  %25 = trunc i32 %24 to i16, !dbg !134
  store i16 %25, i16* %1, align 2, !dbg !135
  br label %31, !dbg !136

; <label>:26:                                     ; preds = %15
  %27 = load i16, i16* %1, align 2, !dbg !137
  %28 = zext i16 %27 to i32, !dbg !137
  %29 = shl i32 %28, 1, !dbg !139
  %30 = trunc i32 %29 to i16, !dbg !140
  store i16 %30, i16* %1, align 2, !dbg !141
  br label %31

; <label>:31:                                     ; preds = %26, %20
  %32 = call i32 (...) @checkpoint(), !dbg !142
  br label %33, !dbg !143

; <label>:33:                                     ; preds = %31
  %34 = load i8, i8* %3, align 1, !dbg !144
  %35 = add i8 %34, -1, !dbg !144
  store i8 %35, i8* %3, align 1, !dbg !144
  br label %11, !dbg !145, !llvm.loop !146

; <label>:36:                                     ; preds = %11
  %37 = load i16, i16* %1, align 2, !dbg !148
  %38 = load i32, i32* %2, align 4, !dbg !149
  %39 = sext i32 %38 to i64, !dbg !150
  %40 = getelementptr inbounds [256 x i16], [256 x i16]* @crcTable, i64 0, i64 %39, !dbg !150
  store i16 %37, i16* %40, align 2, !dbg !151
  %41 = call i32 (...) @checkpoint(), !dbg !152
  br label %42, !dbg !153

; <label>:42:                                     ; preds = %36
  %43 = load i32, i32* %2, align 4, !dbg !154
  %44 = add nsw i32 %43, 1, !dbg !154
  store i32 %44, i32* %2, align 4, !dbg !154
  br label %4, !dbg !155, !llvm.loop !156

; <label>:45:                                     ; preds = %4
  ret void, !dbg !158
}

; Function Attrs: noinline nounwind optnone uwtable
define zeroext i16 @crcFast(i8*, i32) #0 !dbg !159 {
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i16, align 2
  %6 = alloca i8, align 1
  %7 = alloca i32, align 4
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !160, metadata !DIExpression()), !dbg !161
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !162, metadata !DIExpression()), !dbg !163
  call void @llvm.dbg.declare(metadata i16* %5, metadata !164, metadata !DIExpression()), !dbg !165
  store i16 -1, i16* %5, align 2, !dbg !165
  call void @llvm.dbg.declare(metadata i8* %6, metadata !166, metadata !DIExpression()), !dbg !167
  call void @llvm.dbg.declare(metadata i32* %7, metadata !168, metadata !DIExpression()), !dbg !169
  store i32 0, i32* %7, align 4, !dbg !170
  br label %8, !dbg !172

; <label>:8:                                      ; preds = %35, %2
  %9 = load i32, i32* %7, align 4, !dbg !173
  %10 = load i32, i32* %4, align 4, !dbg !175
  %11 = icmp slt i32 %9, %10, !dbg !176
  br i1 %11, label %12, label %38, !dbg !177

; <label>:12:                                     ; preds = %8
  %13 = load i8*, i8** %3, align 8, !dbg !178
  %14 = load i32, i32* %7, align 4, !dbg !178
  %15 = sext i32 %14 to i64, !dbg !178
  %16 = getelementptr inbounds i8, i8* %13, i64 %15, !dbg !178
  %17 = load i8, i8* %16, align 1, !dbg !178
  %18 = zext i8 %17 to i32, !dbg !178
  %19 = load i16, i16* %5, align 2, !dbg !180
  %20 = zext i16 %19 to i32, !dbg !180
  %21 = ashr i32 %20, 8, !dbg !181
  %22 = xor i32 %18, %21, !dbg !182
  %23 = trunc i32 %22 to i8, !dbg !178
  store i8 %23, i8* %6, align 1, !dbg !183
  %24 = load i8, i8* %6, align 1, !dbg !184
  %25 = zext i8 %24 to i64, !dbg !185
  %26 = getelementptr inbounds [256 x i16], [256 x i16]* @crcTable, i64 0, i64 %25, !dbg !185
  %27 = load i16, i16* %26, align 2, !dbg !185
  %28 = zext i16 %27 to i32, !dbg !185
  %29 = load i16, i16* %5, align 2, !dbg !186
  %30 = zext i16 %29 to i32, !dbg !186
  %31 = shl i32 %30, 8, !dbg !187
  %32 = xor i32 %28, %31, !dbg !188
  %33 = trunc i32 %32 to i16, !dbg !185
  store i16 %33, i16* %5, align 2, !dbg !189
  %34 = call i32 (...) @checkpoint(), !dbg !190
  br label %35, !dbg !191

; <label>:35:                                     ; preds = %12
  %36 = load i32, i32* %7, align 4, !dbg !192
  %37 = add nsw i32 %36, 1, !dbg !192
  store i32 %37, i32* %7, align 4, !dbg !192
  br label %8, !dbg !193, !llvm.loop !194

; <label>:38:                                     ; preds = %8
  %39 = load i16, i16* %5, align 2, !dbg !196
  %40 = zext i16 %39 to i32, !dbg !196
  %41 = xor i32 %40, 0, !dbg !197
  %42 = trunc i32 %41 to i16, !dbg !198
  ret i16 %42, !dbg !199
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { argmemonly nounwind }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!12, !2}
!llvm.ident = !{!14, !14}
!llvm.module.flags = !{!15, !16, !17}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "crcTable", scope: !2, file: !3, line: 143, type: !6, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5)
!3 = !DIFile(filename: "crc.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_stack_mini")
!4 = !{}
!5 = !{!0}
!6 = !DICompositeType(tag: DW_TAG_array_type, baseType: !7, size: 4096, elements: !10)
!7 = !DIDerivedType(tag: DW_TAG_typedef, name: "crc", file: !8, line: 31, baseType: !9)
!8 = !DIFile(filename: "./crc.h", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_stack_mini")
!9 = !DIBasicType(name: "unsigned short", size: 16, encoding: DW_ATE_unsigned)
!10 = !{!11}
!11 = !DISubrange(count: 256)
!12 = distinct !DICompileUnit(language: DW_LANG_C99, file: !13, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4)
!13 = !DIFile(filename: "main.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_stack_mini")
!14 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!15 = !{i32 2, !"Dwarf Version", i32 4}
!16 = !{i32 2, !"Debug Info Version", i32 3}
!17 = !{i32 1, !"wchar_size", i32 4}
!18 = distinct !DISubprogram(name: "main", scope: !13, file: !13, line: 23, type: !19, isLocal: false, isDefinition: true, scopeLine: 24, flags: DIFlagPrototyped, isOptimized: false, unit: !12, variables: !4)
!19 = !DISubroutineType(types: !20)
!20 = !{!21}
!21 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!22 = !DILocalVariable(name: "test", scope: !18, file: !13, line: 25, type: !23)
!23 = !DICompositeType(tag: DW_TAG_array_type, baseType: !24, size: 80, elements: !25)
!24 = !DIBasicType(name: "unsigned char", size: 8, encoding: DW_ATE_unsigned_char)
!25 = !{!26}
!26 = !DISubrange(count: 10)
!27 = !DILocation(line: 25, column: 17, scope: !18)
!28 = !DILocation(line: 26, column: 10, scope: !18)
!29 = !DILocation(line: 26, column: 2, scope: !18)
!30 = !DILocation(line: 28, column: 3, scope: !18)
!31 = distinct !DISubprogram(name: "crcSlow", scope: !3, file: !3, line: 97, type: !32, isLocal: false, isDefinition: true, scopeLine: 98, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!32 = !DISubroutineType(types: !33)
!33 = !{!7, !34, !21}
!34 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !35, size: 64)
!35 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !24)
!36 = !DILocalVariable(name: "message", arg: 1, scope: !31, file: !3, line: 97, type: !34)
!37 = !DILocation(line: 97, column: 29, scope: !31)
!38 = !DILocalVariable(name: "nBytes", arg: 2, scope: !31, file: !3, line: 97, type: !21)
!39 = !DILocation(line: 97, column: 44, scope: !31)
!40 = !DILocalVariable(name: "remainder", scope: !31, file: !3, line: 99, type: !7)
!41 = !DILocation(line: 99, column: 20, scope: !31)
!42 = !DILocalVariable(name: "byte", scope: !31, file: !3, line: 100, type: !21)
!43 = !DILocation(line: 100, column: 17, scope: !31)
!44 = !DILocalVariable(name: "bit", scope: !31, file: !3, line: 101, type: !24)
!45 = !DILocation(line: 101, column: 17, scope: !31)
!46 = !DILocation(line: 107, column: 15, scope: !47)
!47 = distinct !DILexicalBlock(scope: !31, file: !3, line: 107, column: 5)
!48 = !DILocation(line: 107, column: 10, scope: !47)
!49 = !DILocation(line: 107, column: 20, scope: !50)
!50 = distinct !DILexicalBlock(scope: !47, file: !3, line: 107, column: 5)
!51 = !DILocation(line: 107, column: 27, scope: !50)
!52 = !DILocation(line: 107, column: 25, scope: !50)
!53 = !DILocation(line: 107, column: 5, scope: !47)
!54 = !DILocation(line: 112, column: 23, scope: !55)
!55 = distinct !DILexicalBlock(scope: !50, file: !3, line: 108, column: 5)
!56 = !DILocation(line: 112, column: 51, scope: !55)
!57 = !DILocation(line: 112, column: 19, scope: !55)
!58 = !DILocation(line: 117, column: 18, scope: !59)
!59 = distinct !DILexicalBlock(scope: !55, file: !3, line: 117, column: 9)
!60 = !DILocation(line: 117, column: 14, scope: !59)
!61 = !DILocation(line: 117, column: 23, scope: !62)
!62 = distinct !DILexicalBlock(scope: !59, file: !3, line: 117, column: 9)
!63 = !DILocation(line: 117, column: 27, scope: !62)
!64 = !DILocation(line: 117, column: 9, scope: !59)
!65 = !DILocation(line: 122, column: 17, scope: !66)
!66 = distinct !DILexicalBlock(scope: !67, file: !3, line: 122, column: 17)
!67 = distinct !DILexicalBlock(scope: !62, file: !3, line: 118, column: 9)
!68 = !DILocation(line: 122, column: 27, scope: !66)
!69 = !DILocation(line: 122, column: 17, scope: !67)
!70 = !DILocation(line: 124, column: 30, scope: !71)
!71 = distinct !DILexicalBlock(scope: !66, file: !3, line: 123, column: 13)
!72 = !DILocation(line: 124, column: 40, scope: !71)
!73 = !DILocation(line: 124, column: 46, scope: !71)
!74 = !DILocation(line: 124, column: 29, scope: !71)
!75 = !DILocation(line: 124, column: 27, scope: !71)
!76 = !DILocation(line: 125, column: 13, scope: !71)
!77 = !DILocation(line: 128, column: 30, scope: !78)
!78 = distinct !DILexicalBlock(scope: !66, file: !3, line: 127, column: 13)
!79 = !DILocation(line: 128, column: 40, scope: !78)
!80 = !DILocation(line: 128, column: 29, scope: !78)
!81 = !DILocation(line: 128, column: 27, scope: !78)
!82 = !DILocation(line: 130, column: 13, scope: !67)
!83 = !DILocation(line: 131, column: 9, scope: !67)
!84 = !DILocation(line: 117, column: 32, scope: !62)
!85 = !DILocation(line: 117, column: 9, scope: !62)
!86 = distinct !{!86, !64, !87}
!87 = !DILocation(line: 131, column: 9, scope: !59)
!88 = !DILocation(line: 132, column: 9, scope: !55)
!89 = !DILocation(line: 133, column: 5, scope: !55)
!90 = !DILocation(line: 107, column: 35, scope: !50)
!91 = !DILocation(line: 107, column: 5, scope: !50)
!92 = distinct !{!92, !53, !93}
!93 = !DILocation(line: 133, column: 5, scope: !47)
!94 = !DILocation(line: 138, column: 13, scope: !31)
!95 = !DILocation(line: 138, column: 42, scope: !31)
!96 = !DILocation(line: 138, column: 12, scope: !31)
!97 = !DILocation(line: 138, column: 5, scope: !31)
!98 = distinct !DISubprogram(name: "crcInit", scope: !3, file: !3, line: 160, type: !99, isLocal: false, isDefinition: true, scopeLine: 161, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!99 = !DISubroutineType(types: !100)
!100 = !{null}
!101 = !DILocalVariable(name: "remainder", scope: !98, file: !3, line: 162, type: !7)
!102 = !DILocation(line: 162, column: 14, scope: !98)
!103 = !DILocalVariable(name: "dividend", scope: !98, file: !3, line: 163, type: !21)
!104 = !DILocation(line: 163, column: 11, scope: !98)
!105 = !DILocalVariable(name: "bit", scope: !98, file: !3, line: 164, type: !24)
!106 = !DILocation(line: 164, column: 17, scope: !98)
!107 = !DILocation(line: 170, column: 19, scope: !108)
!108 = distinct !DILexicalBlock(scope: !98, file: !3, line: 170, column: 5)
!109 = !DILocation(line: 170, column: 10, scope: !108)
!110 = !DILocation(line: 170, column: 24, scope: !111)
!111 = distinct !DILexicalBlock(scope: !108, file: !3, line: 170, column: 5)
!112 = !DILocation(line: 170, column: 33, scope: !111)
!113 = !DILocation(line: 170, column: 5, scope: !108)
!114 = !DILocation(line: 175, column: 21, scope: !115)
!115 = distinct !DILexicalBlock(scope: !111, file: !3, line: 171, column: 5)
!116 = !DILocation(line: 175, column: 30, scope: !115)
!117 = !DILocation(line: 175, column: 19, scope: !115)
!118 = !DILocation(line: 180, column: 18, scope: !119)
!119 = distinct !DILexicalBlock(scope: !115, file: !3, line: 180, column: 9)
!120 = !DILocation(line: 180, column: 14, scope: !119)
!121 = !DILocation(line: 180, column: 23, scope: !122)
!122 = distinct !DILexicalBlock(scope: !119, file: !3, line: 180, column: 9)
!123 = !DILocation(line: 180, column: 27, scope: !122)
!124 = !DILocation(line: 180, column: 9, scope: !119)
!125 = !DILocation(line: 185, column: 17, scope: !126)
!126 = distinct !DILexicalBlock(scope: !127, file: !3, line: 185, column: 17)
!127 = distinct !DILexicalBlock(scope: !122, file: !3, line: 181, column: 9)
!128 = !DILocation(line: 185, column: 27, scope: !126)
!129 = !DILocation(line: 185, column: 17, scope: !127)
!130 = !DILocation(line: 187, column: 30, scope: !131)
!131 = distinct !DILexicalBlock(scope: !126, file: !3, line: 186, column: 13)
!132 = !DILocation(line: 187, column: 40, scope: !131)
!133 = !DILocation(line: 187, column: 46, scope: !131)
!134 = !DILocation(line: 187, column: 29, scope: !131)
!135 = !DILocation(line: 187, column: 27, scope: !131)
!136 = !DILocation(line: 188, column: 13, scope: !131)
!137 = !DILocation(line: 191, column: 30, scope: !138)
!138 = distinct !DILexicalBlock(scope: !126, file: !3, line: 190, column: 13)
!139 = !DILocation(line: 191, column: 40, scope: !138)
!140 = !DILocation(line: 191, column: 29, scope: !138)
!141 = !DILocation(line: 191, column: 27, scope: !138)
!142 = !DILocation(line: 193, column: 13, scope: !127)
!143 = !DILocation(line: 194, column: 9, scope: !127)
!144 = !DILocation(line: 180, column: 32, scope: !122)
!145 = !DILocation(line: 180, column: 9, scope: !122)
!146 = distinct !{!146, !124, !147}
!147 = !DILocation(line: 194, column: 9, scope: !119)
!148 = !DILocation(line: 199, column: 30, scope: !115)
!149 = !DILocation(line: 199, column: 18, scope: !115)
!150 = !DILocation(line: 199, column: 9, scope: !115)
!151 = !DILocation(line: 199, column: 28, scope: !115)
!152 = !DILocation(line: 200, column: 9, scope: !115)
!153 = !DILocation(line: 201, column: 5, scope: !115)
!154 = !DILocation(line: 170, column: 40, scope: !111)
!155 = !DILocation(line: 170, column: 5, scope: !111)
!156 = distinct !{!156, !113, !157}
!157 = !DILocation(line: 201, column: 5, scope: !108)
!158 = !DILocation(line: 203, column: 1, scope: !98)
!159 = distinct !DISubprogram(name: "crcFast", scope: !3, file: !3, line: 218, type: !32, isLocal: false, isDefinition: true, scopeLine: 219, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!160 = !DILocalVariable(name: "message", arg: 1, scope: !159, file: !3, line: 218, type: !34)
!161 = !DILocation(line: 218, column: 29, scope: !159)
!162 = !DILocalVariable(name: "nBytes", arg: 2, scope: !159, file: !3, line: 218, type: !21)
!163 = !DILocation(line: 218, column: 44, scope: !159)
!164 = !DILocalVariable(name: "remainder", scope: !159, file: !3, line: 220, type: !7)
!165 = !DILocation(line: 220, column: 20, scope: !159)
!166 = !DILocalVariable(name: "data", scope: !159, file: !3, line: 221, type: !24)
!167 = !DILocation(line: 221, column: 20, scope: !159)
!168 = !DILocalVariable(name: "byte", scope: !159, file: !3, line: 222, type: !21)
!169 = !DILocation(line: 222, column: 17, scope: !159)
!170 = !DILocation(line: 228, column: 15, scope: !171)
!171 = distinct !DILexicalBlock(scope: !159, file: !3, line: 228, column: 5)
!172 = !DILocation(line: 228, column: 10, scope: !171)
!173 = !DILocation(line: 228, column: 20, scope: !174)
!174 = distinct !DILexicalBlock(scope: !171, file: !3, line: 228, column: 5)
!175 = !DILocation(line: 228, column: 27, scope: !174)
!176 = !DILocation(line: 228, column: 25, scope: !174)
!177 = !DILocation(line: 228, column: 5, scope: !171)
!178 = !DILocation(line: 230, column: 16, scope: !179)
!179 = distinct !DILexicalBlock(scope: !174, file: !3, line: 229, column: 5)
!180 = !DILocation(line: 230, column: 47, scope: !179)
!181 = !DILocation(line: 230, column: 57, scope: !179)
!182 = !DILocation(line: 230, column: 44, scope: !179)
!183 = !DILocation(line: 230, column: 14, scope: !179)
!184 = !DILocation(line: 231, column: 26, scope: !179)
!185 = !DILocation(line: 231, column: 17, scope: !179)
!186 = !DILocation(line: 231, column: 35, scope: !179)
!187 = !DILocation(line: 231, column: 45, scope: !179)
!188 = !DILocation(line: 231, column: 32, scope: !179)
!189 = !DILocation(line: 231, column: 15, scope: !179)
!190 = !DILocation(line: 232, column: 7, scope: !179)
!191 = !DILocation(line: 233, column: 5, scope: !179)
!192 = !DILocation(line: 228, column: 35, scope: !174)
!193 = !DILocation(line: 228, column: 5, scope: !174)
!194 = distinct !{!194, !177, !195}
!195 = !DILocation(line: 233, column: 5, scope: !171)
!196 = !DILocation(line: 238, column: 13, scope: !159)
!197 = !DILocation(line: 238, column: 42, scope: !159)
!198 = !DILocation(line: 238, column: 12, scope: !159)
!199 = !DILocation(line: 238, column: 5, scope: !159)
