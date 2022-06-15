; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@a = global i32 0, align 4, !dbg !0
@b = global i32 0, align 4, !dbg !6

; Function Attrs: noinline nounwind optnone uwtable
define void @variable() #0 !dbg !13 {
  store i32 0, i32* @a, align 4, !dbg !16
  %1 = call i32 (...) @checkpoint(), !dbg !17
  %2 = load i32, i32* @a, align 4, !dbg !18
  store i32 %2, i32* @b, align 4, !dbg !19
  %3 = load i32, i32* @b, align 4, !dbg !20
  %4 = add nsw i32 %3, 1, !dbg !21
  store i32 %4, i32* @b, align 4, !dbg !22
  %5 = load i32, i32* @b, align 4, !dbg !23
  store i32 %5, i32* @a, align 4, !dbg !24
  ret void, !dbg !25
}

declare i32 @checkpoint(...) #1

; Function Attrs: noinline nounwind optnone uwtable
define i32 @stack2() #0 !dbg !26 {
  ret i32 2, !dbg !29
}

; Function Attrs: noinline nounwind optnone uwtable
define i32 @stack() #0 !dbg !30 {
  %1 = call i32 (...) @checkpoint(), !dbg !31
  ret i32 1, !dbg !32
}

; Function Attrs: noinline nounwind optnone uwtable
define void @heap() #0 !dbg !33 {
  %1 = alloca i32*, align 8
  %2 = alloca i32, align 4
  call void @llvm.dbg.declare(metadata i32** %1, metadata !34, metadata !DIExpression()), !dbg !36
  %3 = call i8* @malloc(i64 8), !dbg !37
  %4 = bitcast i8* %3 to i32*, !dbg !37
  store i32* %4, i32** %1, align 8, !dbg !38
  %5 = load i32*, i32** %1, align 8, !dbg !39
  store i32 5, i32* %5, align 4, !dbg !40
  %6 = call i32 (...) @checkpoint(), !dbg !41
  call void @llvm.dbg.declare(metadata i32* %2, metadata !42, metadata !DIExpression()), !dbg !43
  %7 = load i32*, i32** %1, align 8, !dbg !44
  %8 = load i32, i32* %7, align 4, !dbg !45
  %9 = add nsw i32 %8, 7, !dbg !46
  store i32 %9, i32* %2, align 4, !dbg !43
  %10 = load i32*, i32** %1, align 8, !dbg !47
  %11 = call i32 (i32*, ...) bitcast (i32 (...)* @free to i32 (i32*, ...)*)(i32* %10), !dbg !48
  ret void, !dbg !49
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #2

declare i8* @malloc(i64) #1

declare i32 @free(...) #1

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 !dbg !50 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i32 (...) @checkpoint(), !dbg !51
  call void @variable(), !dbg !52
  %3 = call i32 (...) @checkpoint(), !dbg !53
  %4 = call i32 (...) @checkpoint(), !dbg !54
  %5 = call i32 @stack(), !dbg !55
  %6 = call i32 @stack2(), !dbg !56
  %7 = call i32 (...) @checkpoint(), !dbg !57
  %8 = call i32 (...) @checkpoint(), !dbg !58
  call void @heap(), !dbg !59
  %9 = call i32 (...) @checkpoint(), !dbg !60
  ret i32 0, !dbg !61
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readnone speculatable }

!llvm.dbg.cu = !{!2}
!llvm.module.flags = !{!9, !10, !11}
!llvm.ident = !{!12}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "a", scope: !2, file: !3, line: 1, type: !8, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5)
!3 = !DIFile(filename: "source.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/basic_stack")
!4 = !{}
!5 = !{!0, !6}
!6 = !DIGlobalVariableExpression(var: !7, expr: !DIExpression())
!7 = distinct !DIGlobalVariable(name: "b", scope: !2, file: !3, line: 2, type: !8, isLocal: false, isDefinition: true)
!8 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!9 = !{i32 2, !"Dwarf Version", i32 4}
!10 = !{i32 2, !"Debug Info Version", i32 3}
!11 = !{i32 1, !"wchar_size", i32 4}
!12 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!13 = distinct !DISubprogram(name: "variable", scope: !3, file: !3, line: 5, type: !14, isLocal: false, isDefinition: true, scopeLine: 5, isOptimized: false, unit: !2, variables: !4)
!14 = !DISubroutineType(types: !15)
!15 = !{null}
!16 = !DILocation(line: 6, column: 5, scope: !13)
!17 = !DILocation(line: 7, column: 3, scope: !13)
!18 = !DILocation(line: 8, column: 7, scope: !13)
!19 = !DILocation(line: 8, column: 5, scope: !13)
!20 = !DILocation(line: 9, column: 7, scope: !13)
!21 = !DILocation(line: 9, column: 8, scope: !13)
!22 = !DILocation(line: 9, column: 5, scope: !13)
!23 = !DILocation(line: 10, column: 7, scope: !13)
!24 = !DILocation(line: 10, column: 5, scope: !13)
!25 = !DILocation(line: 11, column: 1, scope: !13)
!26 = distinct !DISubprogram(name: "stack2", scope: !3, file: !3, line: 13, type: !27, isLocal: false, isDefinition: true, scopeLine: 13, isOptimized: false, unit: !2, variables: !4)
!27 = !DISubroutineType(types: !28)
!28 = !{!8}
!29 = !DILocation(line: 15, column: 3, scope: !26)
!30 = distinct !DISubprogram(name: "stack", scope: !3, file: !3, line: 18, type: !27, isLocal: false, isDefinition: true, scopeLine: 18, isOptimized: false, unit: !2, variables: !4)
!31 = !DILocation(line: 20, column: 3, scope: !30)
!32 = !DILocation(line: 21, column: 3, scope: !30)
!33 = distinct !DISubprogram(name: "heap", scope: !3, file: !3, line: 24, type: !14, isLocal: false, isDefinition: true, scopeLine: 24, isOptimized: false, unit: !2, variables: !4)
!34 = !DILocalVariable(name: "p", scope: !33, file: !3, line: 25, type: !35)
!35 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !8, size: 64)
!36 = !DILocation(line: 25, column: 8, scope: !33)
!37 = !DILocation(line: 26, column: 7, scope: !33)
!38 = !DILocation(line: 26, column: 5, scope: !33)
!39 = !DILocation(line: 27, column: 4, scope: !33)
!40 = !DILocation(line: 27, column: 5, scope: !33)
!41 = !DILocation(line: 28, column: 3, scope: !33)
!42 = !DILocalVariable(name: "c", scope: !33, file: !3, line: 29, type: !8)
!43 = !DILocation(line: 29, column: 7, scope: !33)
!44 = !DILocation(line: 29, column: 10, scope: !33)
!45 = !DILocation(line: 29, column: 9, scope: !33)
!46 = !DILocation(line: 29, column: 11, scope: !33)
!47 = !DILocation(line: 30, column: 8, scope: !33)
!48 = !DILocation(line: 30, column: 3, scope: !33)
!49 = !DILocation(line: 31, column: 1, scope: !33)
!50 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 33, type: !27, isLocal: false, isDefinition: true, scopeLine: 34, flags: DIFlagPrototyped, isOptimized: false, unit: !2, variables: !4)
!51 = !DILocation(line: 36, column: 3, scope: !50)
!52 = !DILocation(line: 37, column: 3, scope: !50)
!53 = !DILocation(line: 38, column: 3, scope: !50)
!54 = !DILocation(line: 41, column: 3, scope: !50)
!55 = !DILocation(line: 42, column: 3, scope: !50)
!56 = !DILocation(line: 43, column: 3, scope: !50)
!57 = !DILocation(line: 44, column: 3, scope: !50)
!58 = !DILocation(line: 47, column: 3, scope: !50)
!59 = !DILocation(line: 48, column: 3, scope: !50)
!60 = !DILocation(line: 49, column: 3, scope: !50)
!61 = !DILocation(line: 51, column: 3, scope: !50)
