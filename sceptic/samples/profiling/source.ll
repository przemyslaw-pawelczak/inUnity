; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@i = dso_local global i32 0, section ".NVM", align 4, !dbg !0
@.str = private unnamed_addr constant [2 x i8] c"i\00", align 1
@.str.1 = private unnamed_addr constant [12 x i8] c"conditional\00", align 1
@res = dso_local global [100 x i32] zeroinitializer, section ".NVM", align 16, !dbg !6
@.str.2 = private unnamed_addr constant [6 x i8] c"res_i\00", align 1
@.str.3 = private unnamed_addr constant [6 x i8] c"clock\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @main() #0 !dbg !16 {
  store i32 0, i32* @i, align 4, !dbg !19
  %1 = call i32 (...) @checkpoint(), !dbg !20
  br label %2, !dbg !21

; <label>:2:                                      ; preds = %26, %0
  %3 = load i32, i32* @i, align 4, !dbg !22
  %4 = icmp slt i32 %3, 100, !dbg !25
  br i1 %4, label %5, label %29, !dbg !26

; <label>:5:                                      ; preds = %2
  %6 = load i32, i32* @i, align 4, !dbg !27
  %7 = call i32 (i8*, i32, ...) bitcast (i32 (...)* @sceptic_log to i32 (i8*, i32, ...)*)(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i32 0, i32 0), i32 %6), !dbg !29
  %8 = load i32, i32* @i, align 4, !dbg !30
  %9 = icmp eq i32 %8, 3, !dbg !31
  %10 = zext i1 %9 to i32, !dbg !31
  %11 = call i32 (i8*, i32, ...) bitcast (i32 (...)* @sceptic_reset to i32 (i8*, i32, ...)*)(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str.1, i32 0, i32 0), i32 %10), !dbg !32
  %12 = load i32, i32* @i, align 4, !dbg !33
  %13 = load i32, i32* @i, align 4, !dbg !34
  %14 = sext i32 %13 to i64, !dbg !35
  %15 = getelementptr inbounds [100 x i32], [100 x i32]* @res, i64 0, i64 %14, !dbg !35
  store i32 %12, i32* %15, align 4, !dbg !36
  %16 = load i32, i32* @i, align 4, !dbg !37
  %17 = sext i32 %16 to i64, !dbg !38
  %18 = getelementptr inbounds [100 x i32], [100 x i32]* @res, i64 0, i64 %17, !dbg !38
  %19 = load i32, i32* %18, align 4, !dbg !38
  %20 = call i32 (i8*, i32, ...) bitcast (i32 (...)* @sceptic_log to i32 (i8*, i32, ...)*)(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.2, i32 0, i32 0), i32 %19), !dbg !39
  %21 = load i32, i32* @i, align 4, !dbg !40
  %22 = icmp eq i32 %21, 2, !dbg !41
  %23 = zext i1 %22 to i32, !dbg !41
  %24 = call i32 (i8*, i32, ...) bitcast (i32 (...)* @sceptic_reset to i32 (i8*, i32, ...)*)(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @.str.1, i32 0, i32 0), i32 %23), !dbg !42
  %25 = call i32 (i8*, i32, ...) bitcast (i32 (...)* @sceptic_reset to i32 (i8*, i32, ...)*)(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.3, i32 0, i32 0), i32 2), !dbg !43
  br label %26, !dbg !44

; <label>:26:                                     ; preds = %5
  %27 = load i32, i32* @i, align 4, !dbg !45
  %28 = add nsw i32 %27, 1, !dbg !45
  store i32 %28, i32* @i, align 4, !dbg !45
  br label %2, !dbg !46, !llvm.loop !47

; <label>:29:                                     ; preds = %2
  ret void, !dbg !49
}

declare dso_local i32 @checkpoint(...) #1

declare dso_local i32 @sceptic_log(...) #1

declare dso_local i32 @sceptic_reset(...) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!12, !13, !14}
!llvm.ident = !{!15}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "i", scope: !2, file: !3, line: 1, type: !9, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 8.0.0-3 (tags/RELEASE_800/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5, nameTableKind: None)
!3 = !DIFile(filename: "source.c", directory: "/home/sceptic/pysceptic/samples/profiling")
!4 = !{}
!5 = !{!0, !6}
!6 = !DIGlobalVariableExpression(var: !7, expr: !DIExpression())
!7 = distinct !DIGlobalVariable(name: "res", scope: !2, file: !3, line: 2, type: !8, isLocal: false, isDefinition: true)
!8 = !DICompositeType(tag: DW_TAG_array_type, baseType: !9, size: 3200, elements: !10)
!9 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!10 = !{!11}
!11 = !DISubrange(count: 100)
!12 = !{i32 2, !"Dwarf Version", i32 4}
!13 = !{i32 2, !"Debug Info Version", i32 3}
!14 = !{i32 1, !"wchar_size", i32 4}
!15 = !{!"clang version 8.0.0-3 (tags/RELEASE_800/final)"}
!16 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 4, type: !17, scopeLine: 4, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !4)
!17 = !DISubroutineType(types: !18)
!18 = !{null}
!19 = !DILocation(line: 5, column: 7, scope: !16)
!20 = !DILocation(line: 6, column: 5, scope: !16)
!21 = !DILocation(line: 7, column: 5, scope: !16)
!22 = !DILocation(line: 7, column: 11, scope: !23)
!23 = distinct !DILexicalBlock(scope: !24, file: !3, line: 7, column: 5)
!24 = distinct !DILexicalBlock(scope: !16, file: !3, line: 7, column: 5)
!25 = !DILocation(line: 7, column: 13, scope: !23)
!26 = !DILocation(line: 7, column: 5, scope: !24)
!27 = !DILocation(line: 8, column: 26, scope: !28)
!28 = distinct !DILexicalBlock(scope: !23, file: !3, line: 7, column: 25)
!29 = !DILocation(line: 8, column: 9, scope: !28)
!30 = !DILocation(line: 9, column: 38, scope: !28)
!31 = !DILocation(line: 9, column: 40, scope: !28)
!32 = !DILocation(line: 9, column: 9, scope: !28)
!33 = !DILocation(line: 10, column: 18, scope: !28)
!34 = !DILocation(line: 10, column: 13, scope: !28)
!35 = !DILocation(line: 10, column: 9, scope: !28)
!36 = !DILocation(line: 10, column: 16, scope: !28)
!37 = !DILocation(line: 11, column: 34, scope: !28)
!38 = !DILocation(line: 11, column: 30, scope: !28)
!39 = !DILocation(line: 11, column: 9, scope: !28)
!40 = !DILocation(line: 12, column: 38, scope: !28)
!41 = !DILocation(line: 12, column: 40, scope: !28)
!42 = !DILocation(line: 12, column: 9, scope: !28)
!43 = !DILocation(line: 13, column: 9, scope: !28)
!44 = !DILocation(line: 14, column: 5, scope: !28)
!45 = !DILocation(line: 7, column: 21, scope: !23)
!46 = !DILocation(line: 7, column: 5, scope: !23)
!47 = distinct !{!47, !26, !48}
!48 = !DILocation(line: 14, column: 5, scope: !24)
!49 = !DILocation(line: 15, column: 1, scope: !16)
