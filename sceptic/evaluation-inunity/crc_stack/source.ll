; ModuleID = 'llvm-link'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@main.test = private unnamed_addr constant [10 x i8] c"123456789\00", align 1
@.str = private unnamed_addr constant [45 x i8] c"The check value for the %s standard is 0x%X\0A\00", align 1
@.str.1 = private unnamed_addr constant [10 x i8] c"CRC-CCITT\00", align 1
@.str.2 = private unnamed_addr constant [38 x i8] c"The crcSlow() of \22123456789\22 is 0x%X\0A\00", align 1
@.str.3 = private unnamed_addr constant [38 x i8] c"The crcFast() of \22123456789\22 is 0x%X\0A\00", align 1
@crcTable = common global [256 x i16] zeroinitializer, align 16, !dbg !0

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 !dbg !18 {
  %1 = alloca i32, align 4
  %2 = alloca [10 x i8], align 1
  %3 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata [10 x i8]* %2, metadata !22, metadata !DIExpression()), !dbg !27
  %4 = bitcast [10 x i8]* %2 to i8*, !dbg !27
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %4, i8* getelementptr inbounds ([10 x i8], [10 x i8]* @main.test, i32 0, i32 0), i64 10, i32 1, i1 false), !dbg !27
  call void @llvm.dbg.declare(metadata i32* %3, metadata !28, metadata !DIExpression()), !dbg !29
  store i32 9, i32* %3, align 4, !dbg !29
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.1, i32 0, i32 0), i32 10673), !dbg !30
  %6 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !31
  %7 = load i32, i32* %3, align 4, !dbg !32
  %8 = call zeroext i16 @crcSlow(i8* %6, i32 %7), !dbg !33
  %9 = zext i16 %8 to i32, !dbg !33
  %10 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.2, i32 0, i32 0), i32 %9), !dbg !34
  %11 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !35
  %12 = call zeroext i16 @crcSlow(i8* %11, i32 9), !dbg !36
  call void @crcInit(), !dbg !37
  %13 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !38
  %14 = load i32, i32* %3, align 4, !dbg !39
  %15 = call zeroext i16 @crcFast(i8* %13, i32 %14), !dbg !40
  %16 = zext i16 %15 to i32, !dbg !40
  %17 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.3, i32 0, i32 0), i32 %16), !dbg !41
  %18 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !42
  %19 = call zeroext i16 @crcFast(i8* %18, i32 9), !dbg !43
  ret i32 0, !dbg !44
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1) #2

declare i32 @printf(i8*, ...) #3

; Function Attrs: noinline nounwind optnone uwtable
define zeroext i16 @crcSlow(i8*, i32) #0 !dbg !45 {
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i16, align 2
  %6 = alloca i32, align 4
  %7 = alloca i8, align 1
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !50, metadata !DIExpression()), !dbg !51
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !52, metadata !DIExpression()), !dbg !53
  call void @llvm.dbg.declare(metadata i16* %5, metadata !54, metadata !DIExpression()), !dbg !55
  store i16 -1, i16* %5, align 2, !dbg !55
  call void @llvm.dbg.declare(metadata i32* %6, metadata !56, metadata !DIExpression()), !dbg !57
  call void @llvm.dbg.declare(metadata i8* %7, metadata !58, metadata !DIExpression()), !dbg !59
  store i32 0, i32* %6, align 4, !dbg !60
  br label %8, !dbg !62

; <label>:8:                                      ; preds = %51, %2
  %9 = load i32, i32* %6, align 4, !dbg !63
  %10 = load i32, i32* %4, align 4, !dbg !65
  %11 = icmp slt i32 %9, %10, !dbg !66
  br i1 %11, label %12, label %54, !dbg !67

; <label>:12:                                     ; preds = %8
  %13 = load i8*, i8** %3, align 8, !dbg !68
  %14 = load i32, i32* %6, align 4, !dbg !68
  %15 = sext i32 %14 to i64, !dbg !68
  %16 = getelementptr inbounds i8, i8* %13, i64 %15, !dbg !68
  %17 = load i8, i8* %16, align 1, !dbg !68
  %18 = zext i8 %17 to i32, !dbg !68
  %19 = shl i32 %18, 8, !dbg !70
  %20 = load i16, i16* %5, align 2, !dbg !71
  %21 = zext i16 %20 to i32, !dbg !71
  %22 = xor i32 %21, %19, !dbg !71
  %23 = trunc i32 %22 to i16, !dbg !71
  store i16 %23, i16* %5, align 2, !dbg !71
  store i8 8, i8* %7, align 1, !dbg !72
  br label %24, !dbg !74

; <label>:24:                                     ; preds = %46, %12
  %25 = load i8, i8* %7, align 1, !dbg !75
  %26 = zext i8 %25 to i32, !dbg !75
  %27 = icmp sgt i32 %26, 0, !dbg !77
  br i1 %27, label %28, label %49, !dbg !78

; <label>:28:                                     ; preds = %24
  %29 = load i16, i16* %5, align 2, !dbg !79
  %30 = zext i16 %29 to i32, !dbg !79
  %31 = and i32 %30, 32768, !dbg !82
  %32 = icmp ne i32 %31, 0, !dbg !82
  br i1 %32, label %33, label %39, !dbg !83

; <label>:33:                                     ; preds = %28
  %34 = load i16, i16* %5, align 2, !dbg !84
  %35 = zext i16 %34 to i32, !dbg !84
  %36 = shl i32 %35, 1, !dbg !86
  %37 = xor i32 %36, 4129, !dbg !87
  %38 = trunc i32 %37 to i16, !dbg !88
  store i16 %38, i16* %5, align 2, !dbg !89
  br label %44, !dbg !90

; <label>:39:                                     ; preds = %28
  %40 = load i16, i16* %5, align 2, !dbg !91
  %41 = zext i16 %40 to i32, !dbg !91
  %42 = shl i32 %41, 1, !dbg !93
  %43 = trunc i32 %42 to i16, !dbg !94
  store i16 %43, i16* %5, align 2, !dbg !95
  br label %44

; <label>:44:                                     ; preds = %39, %33
  %45 = call i32 (...) @checkpoint(), !dbg !96
  br label %46, !dbg !97

; <label>:46:                                     ; preds = %44
  %47 = load i8, i8* %7, align 1, !dbg !98
  %48 = add i8 %47, -1, !dbg !98
  store i8 %48, i8* %7, align 1, !dbg !98
  br label %24, !dbg !99, !llvm.loop !100

; <label>:49:                                     ; preds = %24
  %50 = call i32 (...) @checkpoint(), !dbg !102
  br label %51, !dbg !103

; <label>:51:                                     ; preds = %49
  %52 = load i32, i32* %6, align 4, !dbg !104
  %53 = add nsw i32 %52, 1, !dbg !104
  store i32 %53, i32* %6, align 4, !dbg !104
  br label %8, !dbg !105, !llvm.loop !106

; <label>:54:                                     ; preds = %8
  %55 = load i16, i16* %5, align 2, !dbg !108
  %56 = zext i16 %55 to i32, !dbg !108
  %57 = xor i32 %56, 0, !dbg !109
  %58 = trunc i32 %57 to i16, !dbg !110
  ret i16 %58, !dbg !111
}

declare i32 @checkpoint(...) #3

; Function Attrs: noinline nounwind optnone uwtable
define void @crcInit() #0 !dbg !112 {
  %1 = alloca i16, align 2
  %2 = alloca i32, align 4
  %3 = alloca i8, align 1
  call void @llvm.dbg.declare(metadata i16* %1, metadata !115, metadata !DIExpression()), !dbg !116
  call void @llvm.dbg.declare(metadata i32* %2, metadata !117, metadata !DIExpression()), !dbg !118
  call void @llvm.dbg.declare(metadata i8* %3, metadata !119, metadata !DIExpression()), !dbg !120
  store i32 0, i32* %2, align 4, !dbg !121
  br label %4, !dbg !123

; <label>:4:                                      ; preds = %42, %0
  %5 = load i32, i32* %2, align 4, !dbg !124
  %6 = icmp slt i32 %5, 256, !dbg !126
  br i1 %6, label %7, label %45, !dbg !127

; <label>:7:                                      ; preds = %4
  %8 = load i32, i32* %2, align 4, !dbg !128
  %9 = shl i32 %8, 8, !dbg !130
  %10 = trunc i32 %9 to i16, !dbg !128
  store i16 %10, i16* %1, align 2, !dbg !131
  store i8 8, i8* %3, align 1, !dbg !132
  br label %11, !dbg !134

; <label>:11:                                     ; preds = %33, %7
  %12 = load i8, i8* %3, align 1, !dbg !135
  %13 = zext i8 %12 to i32, !dbg !135
  %14 = icmp sgt i32 %13, 0, !dbg !137
  br i1 %14, label %15, label %36, !dbg !138

; <label>:15:                                     ; preds = %11
  %16 = load i16, i16* %1, align 2, !dbg !139
  %17 = zext i16 %16 to i32, !dbg !139
  %18 = and i32 %17, 32768, !dbg !142
  %19 = icmp ne i32 %18, 0, !dbg !142
  br i1 %19, label %20, label %26, !dbg !143

; <label>:20:                                     ; preds = %15
  %21 = load i16, i16* %1, align 2, !dbg !144
  %22 = zext i16 %21 to i32, !dbg !144
  %23 = shl i32 %22, 1, !dbg !146
  %24 = xor i32 %23, 4129, !dbg !147
  %25 = trunc i32 %24 to i16, !dbg !148
  store i16 %25, i16* %1, align 2, !dbg !149
  br label %31, !dbg !150

; <label>:26:                                     ; preds = %15
  %27 = load i16, i16* %1, align 2, !dbg !151
  %28 = zext i16 %27 to i32, !dbg !151
  %29 = shl i32 %28, 1, !dbg !153
  %30 = trunc i32 %29 to i16, !dbg !154
  store i16 %30, i16* %1, align 2, !dbg !155
  br label %31

; <label>:31:                                     ; preds = %26, %20
  %32 = call i32 (...) @checkpoint(), !dbg !156
  br label %33, !dbg !157

; <label>:33:                                     ; preds = %31
  %34 = load i8, i8* %3, align 1, !dbg !158
  %35 = add i8 %34, -1, !dbg !158
  store i8 %35, i8* %3, align 1, !dbg !158
  br label %11, !dbg !159, !llvm.loop !160

; <label>:36:                                     ; preds = %11
  %37 = load i16, i16* %1, align 2, !dbg !162
  %38 = load i32, i32* %2, align 4, !dbg !163
  %39 = sext i32 %38 to i64, !dbg !164
  %40 = getelementptr inbounds [256 x i16], [256 x i16]* @crcTable, i64 0, i64 %39, !dbg !164
  store i16 %37, i16* %40, align 2, !dbg !165
  %41 = call i32 (...) @checkpoint(), !dbg !166
  br label %42, !dbg !167

; <label>:42:                                     ; preds = %36
  %43 = load i32, i32* %2, align 4, !dbg !168
  %44 = add nsw i32 %43, 1, !dbg !168
  store i32 %44, i32* %2, align 4, !dbg !168
  br label %4, !dbg !169, !llvm.loop !170

; <label>:45:                                     ; preds = %4
  ret void, !dbg !172
}

; Function Attrs: noinline nounwind optnone uwtable
define zeroext i16 @crcFast(i8*, i32) #0 !dbg !173 {
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i16, align 2
  %6 = alloca i8, align 1
  %7 = alloca i32, align 4
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !174, metadata !DIExpression()), !dbg !175
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !176, metadata !DIExpression()), !dbg !177
  call void @llvm.dbg.declare(metadata i16* %5, metadata !178, metadata !DIExpression()), !dbg !179
  store i16 -1, i16* %5, align 2, !dbg !179
  call void @llvm.dbg.declare(metadata i8* %6, metadata !180, metadata !DIExpression()), !dbg !181
  call void @llvm.dbg.declare(metadata i32* %7, metadata !182, metadata !DIExpression()), !dbg !183
  store i32 0, i32* %7, align 4, !dbg !184
  br label %8, !dbg !186

; <label>:8:                                      ; preds = %35, %2
  %9 = load i32, i32* %7, align 4, !dbg !187
  %10 = load i32, i32* %4, align 4, !dbg !189
  %11 = icmp slt i32 %9, %10, !dbg !190
  br i1 %11, label %12, label %38, !dbg !191

; <label>:12:                                     ; preds = %8
  %13 = load i8*, i8** %3, align 8, !dbg !192
  %14 = load i32, i32* %7, align 4, !dbg !192
  %15 = sext i32 %14 to i64, !dbg !192
  %16 = getelementptr inbounds i8, i8* %13, i64 %15, !dbg !192
  %17 = load i8, i8* %16, align 1, !dbg !192
  %18 = zext i8 %17 to i32, !dbg !192
  %19 = load i16, i16* %5, align 2, !dbg !194
  %20 = zext i16 %19 to i32, !dbg !194
  %21 = ashr i32 %20, 8, !dbg !195
  %22 = xor i32 %18, %21, !dbg !196
  %23 = trunc i32 %22 to i8, !dbg !192
  store i8 %23, i8* %6, align 1, !dbg !197
  %24 = load i8, i8* %6, align 1, !dbg !198
  %25 = zext i8 %24 to i64, !dbg !199
  %26 = getelementptr inbounds [256 x i16], [256 x i16]* @crcTable, i64 0, i64 %25, !dbg !199
  %27 = load i16, i16* %26, align 2, !dbg !199
  %28 = zext i16 %27 to i32, !dbg !199
  %29 = load i16, i16* %5, align 2, !dbg !200
  %30 = zext i16 %29 to i32, !dbg !200
  %31 = shl i32 %30, 8, !dbg !201
  %32 = xor i32 %28, %31, !dbg !202
  %33 = trunc i32 %32 to i16, !dbg !199
  store i16 %33, i16* %5, align 2, !dbg !203
  %34 = call i32 (...) @checkpoint(), !dbg !204
  br label %35, !dbg !205

; <label>:35:                                     ; preds = %12
  %36 = load i32, i32* %7, align 4, !dbg !206
  %37 = add nsw i32 %36, 1, !dbg !206
  store i32 %37, i32* %7, align 4, !dbg !206
  br label %8, !dbg !207, !llvm.loop !208

; <label>:38:                                     ; preds = %8
  %39 = load i16, i16* %5, align 2, !dbg !210
  %40 = zext i16 %39 to i32, !dbg !210
  %41 = xor i32 %40, 0, !dbg !211
  %42 = trunc i32 %41 to i16, !dbg !212
  ret i16 %42, !dbg !213
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
!3 = !DIFile(filename: "crc.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_stack")
!4 = !{}
!5 = !{!0}
!6 = !DICompositeType(tag: DW_TAG_array_type, baseType: !7, size: 4096, elements: !10)
!7 = !DIDerivedType(tag: DW_TAG_typedef, name: "crc", file: !8, line: 31, baseType: !9)
!8 = !DIFile(filename: "./crc.h", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_stack")
!9 = !DIBasicType(name: "unsigned short", size: 16, encoding: DW_ATE_unsigned)
!10 = !{!11}
!11 = !DISubrange(count: 256)
!12 = distinct !DICompileUnit(language: DW_LANG_C99, file: !13, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4)
!13 = !DIFile(filename: "main.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_stack")
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
!28 = !DILocalVariable(name: "length", scope: !18, file: !13, line: 26, type: !21)
!29 = !DILocation(line: 26, column: 6, scope: !18)
!30 = !DILocation(line: 31, column: 2, scope: !18)
!31 = !DILocation(line: 36, column: 61, scope: !18)
!32 = !DILocation(line: 36, column: 67, scope: !18)
!33 = !DILocation(line: 36, column: 53, scope: !18)
!34 = !DILocation(line: 36, column: 2, scope: !18)
!35 = !DILocation(line: 37, column: 11, scope: !18)
!36 = !DILocation(line: 37, column: 3, scope: !18)
!37 = !DILocation(line: 42, column: 2, scope: !18)
!38 = !DILocation(line: 43, column: 61, scope: !18)
!39 = !DILocation(line: 43, column: 67, scope: !18)
!40 = !DILocation(line: 43, column: 53, scope: !18)
!41 = !DILocation(line: 43, column: 2, scope: !18)
!42 = !DILocation(line: 44, column: 11, scope: !18)
!43 = !DILocation(line: 44, column: 3, scope: !18)
!44 = !DILocation(line: 46, column: 3, scope: !18)
!45 = distinct !DISubprogram(name: "crcSlow", scope: !3, file: !3, line: 97, type: !46, isLocal: false, isDefinition: true, scopeLine: 98, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!46 = !DISubroutineType(types: !47)
!47 = !{!7, !48, !21}
!48 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !49, size: 64)
!49 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !24)
!50 = !DILocalVariable(name: "message", arg: 1, scope: !45, file: !3, line: 97, type: !48)
!51 = !DILocation(line: 97, column: 29, scope: !45)
!52 = !DILocalVariable(name: "nBytes", arg: 2, scope: !45, file: !3, line: 97, type: !21)
!53 = !DILocation(line: 97, column: 44, scope: !45)
!54 = !DILocalVariable(name: "remainder", scope: !45, file: !3, line: 99, type: !7)
!55 = !DILocation(line: 99, column: 20, scope: !45)
!56 = !DILocalVariable(name: "byte", scope: !45, file: !3, line: 100, type: !21)
!57 = !DILocation(line: 100, column: 17, scope: !45)
!58 = !DILocalVariable(name: "bit", scope: !45, file: !3, line: 101, type: !24)
!59 = !DILocation(line: 101, column: 17, scope: !45)
!60 = !DILocation(line: 107, column: 15, scope: !61)
!61 = distinct !DILexicalBlock(scope: !45, file: !3, line: 107, column: 5)
!62 = !DILocation(line: 107, column: 10, scope: !61)
!63 = !DILocation(line: 107, column: 20, scope: !64)
!64 = distinct !DILexicalBlock(scope: !61, file: !3, line: 107, column: 5)
!65 = !DILocation(line: 107, column: 27, scope: !64)
!66 = !DILocation(line: 107, column: 25, scope: !64)
!67 = !DILocation(line: 107, column: 5, scope: !61)
!68 = !DILocation(line: 112, column: 23, scope: !69)
!69 = distinct !DILexicalBlock(scope: !64, file: !3, line: 108, column: 5)
!70 = !DILocation(line: 112, column: 51, scope: !69)
!71 = !DILocation(line: 112, column: 19, scope: !69)
!72 = !DILocation(line: 117, column: 18, scope: !73)
!73 = distinct !DILexicalBlock(scope: !69, file: !3, line: 117, column: 9)
!74 = !DILocation(line: 117, column: 14, scope: !73)
!75 = !DILocation(line: 117, column: 23, scope: !76)
!76 = distinct !DILexicalBlock(scope: !73, file: !3, line: 117, column: 9)
!77 = !DILocation(line: 117, column: 27, scope: !76)
!78 = !DILocation(line: 117, column: 9, scope: !73)
!79 = !DILocation(line: 122, column: 17, scope: !80)
!80 = distinct !DILexicalBlock(scope: !81, file: !3, line: 122, column: 17)
!81 = distinct !DILexicalBlock(scope: !76, file: !3, line: 118, column: 9)
!82 = !DILocation(line: 122, column: 27, scope: !80)
!83 = !DILocation(line: 122, column: 17, scope: !81)
!84 = !DILocation(line: 124, column: 30, scope: !85)
!85 = distinct !DILexicalBlock(scope: !80, file: !3, line: 123, column: 13)
!86 = !DILocation(line: 124, column: 40, scope: !85)
!87 = !DILocation(line: 124, column: 46, scope: !85)
!88 = !DILocation(line: 124, column: 29, scope: !85)
!89 = !DILocation(line: 124, column: 27, scope: !85)
!90 = !DILocation(line: 125, column: 13, scope: !85)
!91 = !DILocation(line: 128, column: 30, scope: !92)
!92 = distinct !DILexicalBlock(scope: !80, file: !3, line: 127, column: 13)
!93 = !DILocation(line: 128, column: 40, scope: !92)
!94 = !DILocation(line: 128, column: 29, scope: !92)
!95 = !DILocation(line: 128, column: 27, scope: !92)
!96 = !DILocation(line: 130, column: 13, scope: !81)
!97 = !DILocation(line: 131, column: 9, scope: !81)
!98 = !DILocation(line: 117, column: 32, scope: !76)
!99 = !DILocation(line: 117, column: 9, scope: !76)
!100 = distinct !{!100, !78, !101}
!101 = !DILocation(line: 131, column: 9, scope: !73)
!102 = !DILocation(line: 132, column: 9, scope: !69)
!103 = !DILocation(line: 133, column: 5, scope: !69)
!104 = !DILocation(line: 107, column: 35, scope: !64)
!105 = !DILocation(line: 107, column: 5, scope: !64)
!106 = distinct !{!106, !67, !107}
!107 = !DILocation(line: 133, column: 5, scope: !61)
!108 = !DILocation(line: 138, column: 13, scope: !45)
!109 = !DILocation(line: 138, column: 42, scope: !45)
!110 = !DILocation(line: 138, column: 12, scope: !45)
!111 = !DILocation(line: 138, column: 5, scope: !45)
!112 = distinct !DISubprogram(name: "crcInit", scope: !3, file: !3, line: 160, type: !113, isLocal: false, isDefinition: true, scopeLine: 161, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!113 = !DISubroutineType(types: !114)
!114 = !{null}
!115 = !DILocalVariable(name: "remainder", scope: !112, file: !3, line: 162, type: !7)
!116 = !DILocation(line: 162, column: 14, scope: !112)
!117 = !DILocalVariable(name: "dividend", scope: !112, file: !3, line: 163, type: !21)
!118 = !DILocation(line: 163, column: 11, scope: !112)
!119 = !DILocalVariable(name: "bit", scope: !112, file: !3, line: 164, type: !24)
!120 = !DILocation(line: 164, column: 17, scope: !112)
!121 = !DILocation(line: 170, column: 19, scope: !122)
!122 = distinct !DILexicalBlock(scope: !112, file: !3, line: 170, column: 5)
!123 = !DILocation(line: 170, column: 10, scope: !122)
!124 = !DILocation(line: 170, column: 24, scope: !125)
!125 = distinct !DILexicalBlock(scope: !122, file: !3, line: 170, column: 5)
!126 = !DILocation(line: 170, column: 33, scope: !125)
!127 = !DILocation(line: 170, column: 5, scope: !122)
!128 = !DILocation(line: 175, column: 21, scope: !129)
!129 = distinct !DILexicalBlock(scope: !125, file: !3, line: 171, column: 5)
!130 = !DILocation(line: 175, column: 30, scope: !129)
!131 = !DILocation(line: 175, column: 19, scope: !129)
!132 = !DILocation(line: 180, column: 18, scope: !133)
!133 = distinct !DILexicalBlock(scope: !129, file: !3, line: 180, column: 9)
!134 = !DILocation(line: 180, column: 14, scope: !133)
!135 = !DILocation(line: 180, column: 23, scope: !136)
!136 = distinct !DILexicalBlock(scope: !133, file: !3, line: 180, column: 9)
!137 = !DILocation(line: 180, column: 27, scope: !136)
!138 = !DILocation(line: 180, column: 9, scope: !133)
!139 = !DILocation(line: 185, column: 17, scope: !140)
!140 = distinct !DILexicalBlock(scope: !141, file: !3, line: 185, column: 17)
!141 = distinct !DILexicalBlock(scope: !136, file: !3, line: 181, column: 9)
!142 = !DILocation(line: 185, column: 27, scope: !140)
!143 = !DILocation(line: 185, column: 17, scope: !141)
!144 = !DILocation(line: 187, column: 30, scope: !145)
!145 = distinct !DILexicalBlock(scope: !140, file: !3, line: 186, column: 13)
!146 = !DILocation(line: 187, column: 40, scope: !145)
!147 = !DILocation(line: 187, column: 46, scope: !145)
!148 = !DILocation(line: 187, column: 29, scope: !145)
!149 = !DILocation(line: 187, column: 27, scope: !145)
!150 = !DILocation(line: 188, column: 13, scope: !145)
!151 = !DILocation(line: 191, column: 30, scope: !152)
!152 = distinct !DILexicalBlock(scope: !140, file: !3, line: 190, column: 13)
!153 = !DILocation(line: 191, column: 40, scope: !152)
!154 = !DILocation(line: 191, column: 29, scope: !152)
!155 = !DILocation(line: 191, column: 27, scope: !152)
!156 = !DILocation(line: 193, column: 13, scope: !141)
!157 = !DILocation(line: 194, column: 9, scope: !141)
!158 = !DILocation(line: 180, column: 32, scope: !136)
!159 = !DILocation(line: 180, column: 9, scope: !136)
!160 = distinct !{!160, !138, !161}
!161 = !DILocation(line: 194, column: 9, scope: !133)
!162 = !DILocation(line: 199, column: 30, scope: !129)
!163 = !DILocation(line: 199, column: 18, scope: !129)
!164 = !DILocation(line: 199, column: 9, scope: !129)
!165 = !DILocation(line: 199, column: 28, scope: !129)
!166 = !DILocation(line: 200, column: 9, scope: !129)
!167 = !DILocation(line: 201, column: 5, scope: !129)
!168 = !DILocation(line: 170, column: 40, scope: !125)
!169 = !DILocation(line: 170, column: 5, scope: !125)
!170 = distinct !{!170, !127, !171}
!171 = !DILocation(line: 201, column: 5, scope: !122)
!172 = !DILocation(line: 203, column: 1, scope: !112)
!173 = distinct !DISubprogram(name: "crcFast", scope: !3, file: !3, line: 218, type: !46, isLocal: false, isDefinition: true, scopeLine: 219, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!174 = !DILocalVariable(name: "message", arg: 1, scope: !173, file: !3, line: 218, type: !48)
!175 = !DILocation(line: 218, column: 29, scope: !173)
!176 = !DILocalVariable(name: "nBytes", arg: 2, scope: !173, file: !3, line: 218, type: !21)
!177 = !DILocation(line: 218, column: 44, scope: !173)
!178 = !DILocalVariable(name: "remainder", scope: !173, file: !3, line: 220, type: !7)
!179 = !DILocation(line: 220, column: 20, scope: !173)
!180 = !DILocalVariable(name: "data", scope: !173, file: !3, line: 221, type: !24)
!181 = !DILocation(line: 221, column: 20, scope: !173)
!182 = !DILocalVariable(name: "byte", scope: !173, file: !3, line: 222, type: !21)
!183 = !DILocation(line: 222, column: 17, scope: !173)
!184 = !DILocation(line: 228, column: 15, scope: !185)
!185 = distinct !DILexicalBlock(scope: !173, file: !3, line: 228, column: 5)
!186 = !DILocation(line: 228, column: 10, scope: !185)
!187 = !DILocation(line: 228, column: 20, scope: !188)
!188 = distinct !DILexicalBlock(scope: !185, file: !3, line: 228, column: 5)
!189 = !DILocation(line: 228, column: 27, scope: !188)
!190 = !DILocation(line: 228, column: 25, scope: !188)
!191 = !DILocation(line: 228, column: 5, scope: !185)
!192 = !DILocation(line: 230, column: 16, scope: !193)
!193 = distinct !DILexicalBlock(scope: !188, file: !3, line: 229, column: 5)
!194 = !DILocation(line: 230, column: 47, scope: !193)
!195 = !DILocation(line: 230, column: 57, scope: !193)
!196 = !DILocation(line: 230, column: 44, scope: !193)
!197 = !DILocation(line: 230, column: 14, scope: !193)
!198 = !DILocation(line: 231, column: 26, scope: !193)
!199 = !DILocation(line: 231, column: 17, scope: !193)
!200 = !DILocation(line: 231, column: 35, scope: !193)
!201 = !DILocation(line: 231, column: 45, scope: !193)
!202 = !DILocation(line: 231, column: 32, scope: !193)
!203 = !DILocation(line: 231, column: 15, scope: !193)
!204 = !DILocation(line: 232, column: 7, scope: !193)
!205 = !DILocation(line: 233, column: 5, scope: !193)
!206 = !DILocation(line: 228, column: 35, scope: !188)
!207 = !DILocation(line: 228, column: 5, scope: !188)
!208 = distinct !{!208, !191, !209}
!209 = !DILocation(line: 233, column: 5, scope: !185)
!210 = !DILocation(line: 238, column: 13, scope: !173)
!211 = !DILocation(line: 238, column: 42, scope: !173)
!212 = !DILocation(line: 238, column: 12, scope: !173)
!213 = !DILocation(line: 238, column: 5, scope: !173)
