; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@a = dso_local global i32 5, section ".NVM", align 4, !dbg !0

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 !dbg !11 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata i32* %2, metadata !14, metadata !DIExpression()), !dbg !16
  store i32 0, i32* %2, align 4, !dbg !16
  br label %3, !dbg !17

; <label>:3:                                      ; preds = %10, %0
  %4 = load i32, i32* %2, align 4, !dbg !18
  %5 = icmp slt i32 %4, 10, !dbg !20
  br i1 %5, label %6, label %13, !dbg !21

; <label>:6:                                      ; preds = %3
  %7 = load i32, i32* @a, align 4, !dbg !22
  %8 = add nsw i32 %7, 1, !dbg !22
  store i32 %8, i32* @a, align 4, !dbg !22
  %9 = call i32 (...) @checkpoint(), !dbg !24
  br label %10, !dbg !25

; <label>:10:                                     ; preds = %6
  %11 = load i32, i32* %2, align 4, !dbg !26
  %12 = add nsw i32 %11, 1, !dbg !26
  store i32 %12, i32* %2, align 4, !dbg !26
  br label %3, !dbg !27, !llvm.loop !28

; <label>:13:                                     ; preds = %3
  %14 = load i32, i32* @a, align 4, !dbg !30
  ret i32 %14, !dbg !31
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

declare dso_local i32 @checkpoint(...) #2

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!7, !8, !9}
!llvm.ident = !{!10}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "a", scope: !2, file: !3, line: 1, type: !6, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 8.0.0-3 (tags/RELEASE_800/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5, nameTableKind: None)
!3 = !DIFile(filename: "source.c", directory: "/home/sceptic/pysceptic/samples/memory-locate")
!4 = !{}
!5 = !{!0}
!6 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!7 = !{i32 2, !"Dwarf Version", i32 4}
!8 = !{i32 2, !"Debug Info Version", i32 3}
!9 = !{i32 1, !"wchar_size", i32 4}
!10 = !{!"clang version 8.0.0-3 (tags/RELEASE_800/final)"}
!11 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 4, type: !12, scopeLine: 4, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !4)
!12 = !DISubroutineType(types: !13)
!13 = !{!6}
!14 = !DILocalVariable(name: "i", scope: !15, file: !3, line: 5, type: !6)
!15 = distinct !DILexicalBlock(scope: !11, file: !3, line: 5, column: 5)
!16 = !DILocation(line: 5, column: 13, scope: !15)
!17 = !DILocation(line: 5, column: 9, scope: !15)
!18 = !DILocation(line: 5, column: 20, scope: !19)
!19 = distinct !DILexicalBlock(scope: !15, file: !3, line: 5, column: 5)
!20 = !DILocation(line: 5, column: 22, scope: !19)
!21 = !DILocation(line: 5, column: 5, scope: !15)
!22 = !DILocation(line: 6, column: 10, scope: !23)
!23 = distinct !DILexicalBlock(scope: !19, file: !3, line: 5, column: 33)
!24 = !DILocation(line: 7, column: 2, scope: !23)
!25 = !DILocation(line: 8, column: 5, scope: !23)
!26 = !DILocation(line: 5, column: 29, scope: !19)
!27 = !DILocation(line: 5, column: 5, scope: !19)
!28 = distinct !{!28, !21, !29}
!29 = !DILocation(line: 8, column: 5, scope: !15)
!30 = !DILocation(line: 9, column: 12, scope: !11)
!31 = !DILocation(line: 9, column: 5, scope: !11)
