; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@sum = dso_local global i32 0, align 4, !dbg !0
@critical = dso_local global i32 10000, align 4, !dbg !6
@i = common dso_local global i32 0, align 4, !dbg !9
@val = common dso_local global i32 0, align 4, !dbg !11

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 !dbg !17 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 0, i32* @i, align 4, !dbg !20
  br label %2, !dbg !22

; <label>:2:                                      ; preds = %17, %0
  %3 = load i32, i32* @i, align 4, !dbg !23
  %4 = icmp slt i32 %3, 50, !dbg !25
  br i1 %4, label %5, label %20, !dbg !26

; <label>:5:                                      ; preds = %2
  %6 = call i32 (...) @input(), !dbg !27
  store i32 %6, i32* @val, align 4, !dbg !29
  %7 = call i32 (...) @checkpoint(), !dbg !30
  %8 = load i32, i32* @sum, align 4, !dbg !31
  %9 = load i32, i32* @val, align 4, !dbg !32
  %10 = add nsw i32 %8, %9, !dbg !33
  store i32 %10, i32* @sum, align 4, !dbg !34
  %11 = load i32, i32* @sum, align 4, !dbg !35
  %12 = load i32, i32* @critical, align 4, !dbg !37
  %13 = icmp sgt i32 %11, %12, !dbg !38
  br i1 %13, label %14, label %16, !dbg !39

; <label>:14:                                     ; preds = %5
  %15 = call i32 (i32, ...) bitcast (i32 (...)* @out to i32 (i32, ...)*)(i32 1684366369), !dbg !40
  br label %16, !dbg !42

; <label>:16:                                     ; preds = %14, %5
  br label %17, !dbg !43

; <label>:17:                                     ; preds = %16
  %18 = load i32, i32* @i, align 4, !dbg !44
  %19 = add nsw i32 %18, 1, !dbg !44
  store i32 %19, i32* @i, align 4, !dbg !44
  br label %2, !dbg !45, !llvm.loop !46

; <label>:20:                                     ; preds = %2
  %21 = load i32, i32* @sum, align 4, !dbg !48
  %22 = call i32 (i32, ...) bitcast (i32 (...)* @out to i32 (i32, ...)*)(i32 %21), !dbg !49
  %23 = load i32, i32* %1, align 4, !dbg !50
  ret i32 %23, !dbg !50
}

declare dso_local i32 @input(...) #1

declare dso_local i32 @checkpoint(...) #1

declare dso_local i32 @out(...) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!13, !14, !15}
!llvm.ident = !{!16}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "sum", scope: !2, file: !3, line: 3, type: !8, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 8.0.0-3 (tags/RELEASE_800/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5, nameTableKind: None)
!3 = !DIFile(filename: "source.c", directory: "/home/sceptic/pysceptic/samples/input")
!4 = !{}
!5 = !{!0, !6, !9, !11}
!6 = !DIGlobalVariableExpression(var: !7, expr: !DIExpression())
!7 = distinct !DIGlobalVariable(name: "critical", scope: !2, file: !3, line: 4, type: !8, isLocal: false, isDefinition: true)
!8 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!9 = !DIGlobalVariableExpression(var: !10, expr: !DIExpression())
!10 = distinct !DIGlobalVariable(name: "i", scope: !2, file: !3, line: 1, type: !8, isLocal: false, isDefinition: true)
!11 = !DIGlobalVariableExpression(var: !12, expr: !DIExpression())
!12 = distinct !DIGlobalVariable(name: "val", scope: !2, file: !3, line: 2, type: !8, isLocal: false, isDefinition: true)
!13 = !{i32 2, !"Dwarf Version", i32 4}
!14 = !{i32 2, !"Debug Info Version", i32 3}
!15 = !{i32 1, !"wchar_size", i32 4}
!16 = !{!"clang version 8.0.0-3 (tags/RELEASE_800/final)"}
!17 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 6, type: !18, scopeLine: 6, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !4)
!18 = !DISubroutineType(types: !19)
!19 = !{!8}
!20 = !DILocation(line: 7, column: 8, scope: !21)
!21 = distinct !DILexicalBlock(scope: !17, file: !3, line: 7, column: 2)
!22 = !DILocation(line: 7, column: 6, scope: !21)
!23 = !DILocation(line: 7, column: 13, scope: !24)
!24 = distinct !DILexicalBlock(scope: !21, file: !3, line: 7, column: 2)
!25 = !DILocation(line: 7, column: 15, scope: !24)
!26 = !DILocation(line: 7, column: 2, scope: !21)
!27 = !DILocation(line: 8, column: 9, scope: !28)
!28 = distinct !DILexicalBlock(scope: !24, file: !3, line: 7, column: 26)
!29 = !DILocation(line: 8, column: 7, scope: !28)
!30 = !DILocation(line: 9, column: 3, scope: !28)
!31 = !DILocation(line: 10, column: 9, scope: !28)
!32 = !DILocation(line: 10, column: 15, scope: !28)
!33 = !DILocation(line: 10, column: 13, scope: !28)
!34 = !DILocation(line: 10, column: 7, scope: !28)
!35 = !DILocation(line: 12, column: 6, scope: !36)
!36 = distinct !DILexicalBlock(scope: !28, file: !3, line: 12, column: 6)
!37 = !DILocation(line: 12, column: 12, scope: !36)
!38 = !DILocation(line: 12, column: 10, scope: !36)
!39 = !DILocation(line: 12, column: 6, scope: !28)
!40 = !DILocation(line: 13, column: 4, scope: !41)
!41 = distinct !DILexicalBlock(scope: !36, file: !3, line: 12, column: 22)
!42 = !DILocation(line: 14, column: 3, scope: !41)
!43 = !DILocation(line: 15, column: 2, scope: !28)
!44 = !DILocation(line: 7, column: 22, scope: !24)
!45 = !DILocation(line: 7, column: 2, scope: !24)
!46 = distinct !{!46, !26, !47}
!47 = !DILocation(line: 15, column: 2, scope: !21)
!48 = !DILocation(line: 17, column: 6, scope: !17)
!49 = !DILocation(line: 17, column: 2, scope: !17)
!50 = !DILocation(line: 18, column: 1, scope: !17)
