; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@sum = dso_local global i32 0, align 4, !dbg !0
@i = common dso_local global i32 0, align 4, !dbg !6
@val = common dso_local global i32 0, align 4, !dbg !9

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 !dbg !15 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 0, i32* @i, align 4, !dbg !18
  br label %2, !dbg !20

; <label>:2:                                      ; preds = %14, %0
  %3 = load i32, i32* @i, align 4, !dbg !21
  %4 = icmp slt i32 %3, 50, !dbg !23
  br i1 %4, label %5, label %17, !dbg !24

; <label>:5:                                      ; preds = %2
  %6 = call i32 (...) @input(), !dbg !25
  store i32 %6, i32* @val, align 4, !dbg !27
  %7 = call i32 (...) @checkpoint(), !dbg !28
  %8 = load i32, i32* @sum, align 4, !dbg !29
  %9 = load i32, i32* @val, align 4, !dbg !30
  %10 = add nsw i32 %8, %9, !dbg !31
  store i32 %10, i32* @sum, align 4, !dbg !32
  %11 = call i32 (i32, ...) bitcast (i32 (...)* @out1 to i32 (i32, ...)*)(i32 1), !dbg !33
  %12 = load i32, i32* @sum, align 4, !dbg !34
  %13 = call i32 (i32, ...) bitcast (i32 (...)* @out2 to i32 (i32, ...)*)(i32 %12), !dbg !35
  br label %14, !dbg !36

; <label>:14:                                     ; preds = %5
  %15 = load i32, i32* @i, align 4, !dbg !37
  %16 = add nsw i32 %15, 1, !dbg !37
  store i32 %16, i32* @i, align 4, !dbg !37
  br label %2, !dbg !38, !llvm.loop !39

; <label>:17:                                     ; preds = %2
  %18 = load i32, i32* %1, align 4, !dbg !41
  ret i32 %18, !dbg !41
}

declare dso_local i32 @input(...) #1

declare dso_local i32 @checkpoint(...) #1

declare dso_local i32 @out1(...) #1

declare dso_local i32 @out2(...) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!11, !12, !13}
!llvm.ident = !{!14}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "sum", scope: !2, file: !3, line: 3, type: !8, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 8.0.0-3 (tags/RELEASE_800/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5, nameTableKind: None)
!3 = !DIFile(filename: "source.c", directory: "/home/sceptic/pysceptic/samples/output")
!4 = !{}
!5 = !{!0, !6, !9}
!6 = !DIGlobalVariableExpression(var: !7, expr: !DIExpression())
!7 = distinct !DIGlobalVariable(name: "i", scope: !2, file: !3, line: 1, type: !8, isLocal: false, isDefinition: true)
!8 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!9 = !DIGlobalVariableExpression(var: !10, expr: !DIExpression())
!10 = distinct !DIGlobalVariable(name: "val", scope: !2, file: !3, line: 2, type: !8, isLocal: false, isDefinition: true)
!11 = !{i32 2, !"Dwarf Version", i32 4}
!12 = !{i32 2, !"Debug Info Version", i32 3}
!13 = !{i32 1, !"wchar_size", i32 4}
!14 = !{!"clang version 8.0.0-3 (tags/RELEASE_800/final)"}
!15 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 5, type: !16, scopeLine: 5, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !4)
!16 = !DISubroutineType(types: !17)
!17 = !{!8}
!18 = !DILocation(line: 6, column: 8, scope: !19)
!19 = distinct !DILexicalBlock(scope: !15, file: !3, line: 6, column: 2)
!20 = !DILocation(line: 6, column: 6, scope: !19)
!21 = !DILocation(line: 6, column: 13, scope: !22)
!22 = distinct !DILexicalBlock(scope: !19, file: !3, line: 6, column: 2)
!23 = !DILocation(line: 6, column: 15, scope: !22)
!24 = !DILocation(line: 6, column: 2, scope: !19)
!25 = !DILocation(line: 7, column: 9, scope: !26)
!26 = distinct !DILexicalBlock(scope: !22, file: !3, line: 6, column: 26)
!27 = !DILocation(line: 7, column: 7, scope: !26)
!28 = !DILocation(line: 8, column: 3, scope: !26)
!29 = !DILocation(line: 9, column: 9, scope: !26)
!30 = !DILocation(line: 9, column: 15, scope: !26)
!31 = !DILocation(line: 9, column: 13, scope: !26)
!32 = !DILocation(line: 9, column: 7, scope: !26)
!33 = !DILocation(line: 10, column: 3, scope: !26)
!34 = !DILocation(line: 11, column: 8, scope: !26)
!35 = !DILocation(line: 11, column: 3, scope: !26)
!36 = !DILocation(line: 12, column: 2, scope: !26)
!37 = !DILocation(line: 6, column: 22, scope: !22)
!38 = !DILocation(line: 6, column: 2, scope: !22)
!39 = distinct !{!39, !24, !40}
!40 = !DILocation(line: 12, column: 2, scope: !19)
!41 = !DILocation(line: 13, column: 1, scope: !15)
