; ModuleID = 'main.c'
source_filename = "main.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@main.test = private unnamed_addr constant [10 x i8] c"123456789\00", align 1
@.str = private unnamed_addr constant [45 x i8] c"The check value for the %s standard is 0x%X\0A\00", align 1
@.str.1 = private unnamed_addr constant [10 x i8] c"CRC-CCITT\00", align 1
@.str.2 = private unnamed_addr constant [38 x i8] c"The crcSlow() of \22123456789\22 is 0x%X\0A\00", align 1
@.str.3 = private unnamed_addr constant [38 x i8] c"The crcFast() of \22123456789\22 is 0x%X\0A\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 !dbg !7 {
  %1 = alloca i32, align 4
  %2 = alloca [10 x i8], align 1
  %3 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata [10 x i8]* %2, metadata !11, metadata !DIExpression()), !dbg !16
  %4 = bitcast [10 x i8]* %2 to i8*, !dbg !16
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %4, i8* getelementptr inbounds ([10 x i8], [10 x i8]* @main.test, i32 0, i32 0), i64 10, i32 1, i1 false), !dbg !16
  call void @llvm.dbg.declare(metadata i32* %3, metadata !17, metadata !DIExpression()), !dbg !18
  store i32 9, i32* %3, align 4, !dbg !18
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.1, i32 0, i32 0), i32 10673), !dbg !19
  %6 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !20
  %7 = load i32, i32* %3, align 4, !dbg !21
  %8 = call zeroext i16 @crcSlow(i8* %6, i32 %7), !dbg !22
  %9 = zext i16 %8 to i32, !dbg !22
  %10 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.2, i32 0, i32 0), i32 %9), !dbg !23
  %11 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !24
  %12 = call zeroext i16 @crcSlow(i8* %11, i32 9), !dbg !25
  call void @crcInit(), !dbg !26
  %13 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !27
  %14 = load i32, i32* %3, align 4, !dbg !28
  %15 = call zeroext i16 @crcFast(i8* %13, i32 %14), !dbg !29
  %16 = zext i16 %15 to i32, !dbg !29
  %17 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.3, i32 0, i32 0), i32 %16), !dbg !30
  %18 = getelementptr inbounds [10 x i8], [10 x i8]* %2, i32 0, i32 0, !dbg !31
  %19 = call zeroext i16 @crcFast(i8* %18, i32 9), !dbg !32
  ret i32 0, !dbg !33
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1) #2

declare i32 @printf(i8*, ...) #3

declare zeroext i16 @crcSlow(i8*, i32) #3

declare void @crcInit() #3

declare zeroext i16 @crcFast(i8*, i32) #3

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { argmemonly nounwind }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2)
!1 = !DIFile(filename: "main.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/crc_global")
!2 = !{}
!3 = !{i32 2, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!7 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 23, type: !8, isLocal: false, isDefinition: true, scopeLine: 24, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!8 = !DISubroutineType(types: !9)
!9 = !{!10}
!10 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!11 = !DILocalVariable(name: "test", scope: !7, file: !1, line: 25, type: !12)
!12 = !DICompositeType(tag: DW_TAG_array_type, baseType: !13, size: 80, elements: !14)
!13 = !DIBasicType(name: "unsigned char", size: 8, encoding: DW_ATE_unsigned_char)
!14 = !{!15}
!15 = !DISubrange(count: 10)
!16 = !DILocation(line: 25, column: 17, scope: !7)
!17 = !DILocalVariable(name: "length", scope: !7, file: !1, line: 26, type: !10)
!18 = !DILocation(line: 26, column: 6, scope: !7)
!19 = !DILocation(line: 31, column: 2, scope: !7)
!20 = !DILocation(line: 36, column: 61, scope: !7)
!21 = !DILocation(line: 36, column: 67, scope: !7)
!22 = !DILocation(line: 36, column: 53, scope: !7)
!23 = !DILocation(line: 36, column: 2, scope: !7)
!24 = !DILocation(line: 37, column: 11, scope: !7)
!25 = !DILocation(line: 37, column: 3, scope: !7)
!26 = !DILocation(line: 42, column: 2, scope: !7)
!27 = !DILocation(line: 43, column: 61, scope: !7)
!28 = !DILocation(line: 43, column: 67, scope: !7)
!29 = !DILocation(line: 43, column: 53, scope: !7)
!30 = !DILocation(line: 43, column: 2, scope: !7)
!31 = !DILocation(line: 44, column: 11, scope: !7)
!32 = !DILocation(line: 44, column: 3, scope: !7)
!33 = !DILocation(line: 46, column: 3, scope: !7)
