; ModuleID = 'fftmisc.c'
source_filename = "fftmisc.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind optnone uwtable
define i32 @IsPowerOfTwo(i32) #0 !dbg !9 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !14, metadata !DIExpression()), !dbg !15
  %4 = load i32, i32* %3, align 4, !dbg !16
  %5 = icmp ult i32 %4, 2, !dbg !18
  br i1 %5, label %6, label %7, !dbg !19

; <label>:6:                                      ; preds = %1
  store i32 0, i32* %2, align 4, !dbg !20
  br label %15, !dbg !20

; <label>:7:                                      ; preds = %1
  %8 = load i32, i32* %3, align 4, !dbg !21
  %9 = load i32, i32* %3, align 4, !dbg !23
  %10 = sub i32 %9, 1, !dbg !24
  %11 = and i32 %8, %10, !dbg !25
  %12 = icmp ne i32 %11, 0, !dbg !25
  br i1 %12, label %13, label %14, !dbg !26

; <label>:13:                                     ; preds = %7
  store i32 0, i32* %2, align 4, !dbg !27
  br label %15, !dbg !27

; <label>:14:                                     ; preds = %7
  store i32 1, i32* %2, align 4, !dbg !28
  br label %15, !dbg !28

; <label>:15:                                     ; preds = %14, %13, %6
  %16 = load i32, i32* %2, align 4, !dbg !29
  ret i32 %16, !dbg !29
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline nounwind optnone uwtable
define i32 @NumberOfBitsNeeded(i32) #0 !dbg !30 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  call void @llvm.dbg.declare(metadata i32* %2, metadata !33, metadata !DIExpression()), !dbg !34
  call void @llvm.dbg.declare(metadata i32* %3, metadata !35, metadata !DIExpression()), !dbg !36
  %4 = load i32, i32* %2, align 4, !dbg !37
  %5 = icmp ult i32 %4, 2, !dbg !39
  br i1 %5, label %6, label %7, !dbg !40

; <label>:6:                                      ; preds = %1
  call void @exit(i32 1) #4, !dbg !41
  unreachable, !dbg !41

; <label>:7:                                      ; preds = %1
  store i32 0, i32* %3, align 4, !dbg !43
  br label %8, !dbg !45

; <label>:8:                                      ; preds = %18, %7
  %9 = load i32, i32* %2, align 4, !dbg !46
  %10 = load i32, i32* %3, align 4, !dbg !50
  %11 = shl i32 1, %10, !dbg !51
  %12 = and i32 %9, %11, !dbg !52
  %13 = icmp ne i32 %12, 0, !dbg !52
  br i1 %13, label %14, label %16, !dbg !53

; <label>:14:                                     ; preds = %8
  %15 = load i32, i32* %3, align 4, !dbg !54
  ret i32 %15, !dbg !55

; <label>:16:                                     ; preds = %8
  %17 = call i32 (...) @checkpoint(), !dbg !56
  br label %18, !dbg !57

; <label>:18:                                     ; preds = %16
  %19 = load i32, i32* %3, align 4, !dbg !58
  %20 = add i32 %19, 1, !dbg !58
  store i32 %20, i32* %3, align 4, !dbg !58
  br label %8, !dbg !59, !llvm.loop !60
}

; Function Attrs: noreturn nounwind
declare void @exit(i32) #2

declare i32 @checkpoint(...) #3

; Function Attrs: noinline nounwind optnone uwtable
define i32 @ReverseBits(i32, i32) #0 !dbg !63 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !66, metadata !DIExpression()), !dbg !67
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !68, metadata !DIExpression()), !dbg !69
  call void @llvm.dbg.declare(metadata i32* %5, metadata !70, metadata !DIExpression()), !dbg !71
  call void @llvm.dbg.declare(metadata i32* %6, metadata !72, metadata !DIExpression()), !dbg !73
  store i32 0, i32* %6, align 4, !dbg !74
  store i32 0, i32* %5, align 4, !dbg !76
  br label %7, !dbg !77

; <label>:7:                                      ; preds = %20, %2
  %8 = load i32, i32* %5, align 4, !dbg !78
  %9 = load i32, i32* %4, align 4, !dbg !80
  %10 = icmp ult i32 %8, %9, !dbg !81
  br i1 %10, label %11, label %23, !dbg !82

; <label>:11:                                     ; preds = %7
  %12 = load i32, i32* %6, align 4, !dbg !83
  %13 = shl i32 %12, 1, !dbg !85
  %14 = load i32, i32* %3, align 4, !dbg !86
  %15 = and i32 %14, 1, !dbg !87
  %16 = or i32 %13, %15, !dbg !88
  store i32 %16, i32* %6, align 4, !dbg !89
  %17 = load i32, i32* %3, align 4, !dbg !90
  %18 = lshr i32 %17, 1, !dbg !90
  store i32 %18, i32* %3, align 4, !dbg !90
  %19 = call i32 (...) @checkpoint(), !dbg !91
  br label %20, !dbg !92

; <label>:20:                                     ; preds = %11
  %21 = load i32, i32* %5, align 4, !dbg !93
  %22 = add i32 %21, 1, !dbg !93
  store i32 %22, i32* %5, align 4, !dbg !93
  br label %7, !dbg !94, !llvm.loop !95

; <label>:23:                                     ; preds = %7
  %24 = load i32, i32* %6, align 4, !dbg !97
  ret i32 %24, !dbg !98
}

; Function Attrs: noinline nounwind optnone uwtable
define double @Index_to_frequency(i32, i32) #0 !dbg !99 {
  %3 = alloca double, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !102, metadata !DIExpression()), !dbg !103
  store i32 %1, i32* %5, align 4
  call void @llvm.dbg.declare(metadata i32* %5, metadata !104, metadata !DIExpression()), !dbg !105
  %6 = load i32, i32* %5, align 4, !dbg !106
  %7 = load i32, i32* %4, align 4, !dbg !108
  %8 = icmp uge i32 %6, %7, !dbg !109
  br i1 %8, label %9, label %10, !dbg !110

; <label>:9:                                      ; preds = %2
  store double 0.000000e+00, double* %3, align 8, !dbg !111
  br label %31, !dbg !111

; <label>:10:                                     ; preds = %2
  %11 = load i32, i32* %5, align 4, !dbg !112
  %12 = load i32, i32* %4, align 4, !dbg !114
  %13 = udiv i32 %12, 2, !dbg !115
  %14 = icmp ule i32 %11, %13, !dbg !116
  br i1 %14, label %15, label %21, !dbg !117

; <label>:15:                                     ; preds = %10
  %16 = load i32, i32* %5, align 4, !dbg !118
  %17 = uitofp i32 %16 to double, !dbg !119
  %18 = load i32, i32* %4, align 4, !dbg !120
  %19 = uitofp i32 %18 to double, !dbg !121
  %20 = fdiv double %17, %19, !dbg !122
  store double %20, double* %3, align 8, !dbg !123
  br label %31, !dbg !123

; <label>:21:                                     ; preds = %10
  br label %22

; <label>:22:                                     ; preds = %21
  %23 = load i32, i32* %4, align 4, !dbg !124
  %24 = load i32, i32* %5, align 4, !dbg !125
  %25 = sub i32 %23, %24, !dbg !126
  %26 = uitofp i32 %25 to double, !dbg !127
  %27 = fsub double -0.000000e+00, %26, !dbg !128
  %28 = load i32, i32* %4, align 4, !dbg !129
  %29 = uitofp i32 %28 to double, !dbg !130
  %30 = fdiv double %27, %29, !dbg !131
  store double %30, double* %3, align 8, !dbg !132
  br label %31, !dbg !132

; <label>:31:                                     ; preds = %22, %15, %9
  %32 = load double, double* %3, align 8, !dbg !133
  ret double %32, !dbg !133
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { noreturn nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noreturn nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!5, !6, !7}
!llvm.ident = !{!8}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, retainedTypes: !3)
!1 = !DIFile(filename: "fftmisc.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/fft_stack")
!2 = !{}
!3 = !{!4}
!4 = !DIBasicType(name: "double", size: 64, encoding: DW_ATE_float)
!5 = !{i32 2, !"Dwarf Version", i32 4}
!6 = !{i32 2, !"Debug Info Version", i32 3}
!7 = !{i32 1, !"wchar_size", i32 4}
!8 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!9 = distinct !DISubprogram(name: "IsPowerOfTwo", scope: !1, file: !1, line: 35, type: !10, isLocal: false, isDefinition: true, scopeLine: 36, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!10 = !DISubroutineType(types: !11)
!11 = !{!12, !13}
!12 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!13 = !DIBasicType(name: "unsigned int", size: 32, encoding: DW_ATE_unsigned)
!14 = !DILocalVariable(name: "x", arg: 1, scope: !9, file: !1, line: 35, type: !13)
!15 = !DILocation(line: 35, column: 29, scope: !9)
!16 = !DILocation(line: 37, column: 10, scope: !17)
!17 = distinct !DILexicalBlock(scope: !9, file: !1, line: 37, column: 10)
!18 = !DILocation(line: 37, column: 12, scope: !17)
!19 = !DILocation(line: 37, column: 10, scope: !9)
!20 = !DILocation(line: 38, column: 9, scope: !17)
!21 = !DILocation(line: 40, column: 10, scope: !22)
!22 = distinct !DILexicalBlock(scope: !9, file: !1, line: 40, column: 10)
!23 = !DILocation(line: 40, column: 15, scope: !22)
!24 = !DILocation(line: 40, column: 16, scope: !22)
!25 = !DILocation(line: 40, column: 12, scope: !22)
!26 = !DILocation(line: 40, column: 10, scope: !9)
!27 = !DILocation(line: 41, column: 9, scope: !22)
!28 = !DILocation(line: 43, column: 5, scope: !9)
!29 = !DILocation(line: 44, column: 1, scope: !9)
!30 = distinct !DISubprogram(name: "NumberOfBitsNeeded", scope: !1, file: !1, line: 47, type: !31, isLocal: false, isDefinition: true, scopeLine: 48, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!31 = !DISubroutineType(types: !32)
!32 = !{!13, !13}
!33 = !DILocalVariable(name: "PowerOfTwo", arg: 1, scope: !30, file: !1, line: 47, type: !13)
!34 = !DILocation(line: 47, column: 40, scope: !30)
!35 = !DILocalVariable(name: "i", scope: !30, file: !1, line: 49, type: !13)
!36 = !DILocation(line: 49, column: 14, scope: !30)
!37 = !DILocation(line: 51, column: 10, scope: !38)
!38 = distinct !DILexicalBlock(scope: !30, file: !1, line: 51, column: 10)
!39 = !DILocation(line: 51, column: 21, scope: !38)
!40 = !DILocation(line: 51, column: 10, scope: !30)
!41 = !DILocation(line: 58, column: 9, scope: !42)
!42 = distinct !DILexicalBlock(scope: !38, file: !1, line: 52, column: 5)
!43 = !DILocation(line: 61, column: 12, scope: !44)
!44 = distinct !DILexicalBlock(scope: !30, file: !1, line: 61, column: 5)
!45 = !DILocation(line: 61, column: 11, scope: !44)
!46 = !DILocation(line: 63, column: 14, scope: !47)
!47 = distinct !DILexicalBlock(scope: !48, file: !1, line: 63, column: 14)
!48 = distinct !DILexicalBlock(scope: !49, file: !1, line: 62, column: 5)
!49 = distinct !DILexicalBlock(scope: !44, file: !1, line: 61, column: 5)
!50 = !DILocation(line: 63, column: 33, scope: !47)
!51 = !DILocation(line: 63, column: 30, scope: !47)
!52 = !DILocation(line: 63, column: 25, scope: !47)
!53 = !DILocation(line: 63, column: 14, scope: !48)
!54 = !DILocation(line: 64, column: 20, scope: !47)
!55 = !DILocation(line: 64, column: 13, scope: !47)
!56 = !DILocation(line: 66, column: 9, scope: !48)
!57 = !DILocation(line: 67, column: 5, scope: !48)
!58 = !DILocation(line: 61, column: 19, scope: !49)
!59 = !DILocation(line: 61, column: 5, scope: !49)
!60 = distinct !{!60, !61, !62}
!61 = !DILocation(line: 61, column: 5, scope: !44)
!62 = !DILocation(line: 67, column: 5, scope: !44)
!63 = distinct !DISubprogram(name: "ReverseBits", scope: !1, file: !1, line: 72, type: !64, isLocal: false, isDefinition: true, scopeLine: 73, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!64 = !DISubroutineType(types: !65)
!65 = !{!13, !13, !13}
!66 = !DILocalVariable(name: "index", arg: 1, scope: !63, file: !1, line: 72, type: !13)
!67 = !DILocation(line: 72, column: 33, scope: !63)
!68 = !DILocalVariable(name: "NumBits", arg: 2, scope: !63, file: !1, line: 72, type: !13)
!69 = !DILocation(line: 72, column: 49, scope: !63)
!70 = !DILocalVariable(name: "i", scope: !63, file: !1, line: 74, type: !13)
!71 = !DILocation(line: 74, column: 14, scope: !63)
!72 = !DILocalVariable(name: "rev", scope: !63, file: !1, line: 74, type: !13)
!73 = !DILocation(line: 74, column: 17, scope: !63)
!74 = !DILocation(line: 76, column: 16, scope: !75)
!75 = distinct !DILexicalBlock(scope: !63, file: !1, line: 76, column: 5)
!76 = !DILocation(line: 76, column: 12, scope: !75)
!77 = !DILocation(line: 76, column: 11, scope: !75)
!78 = !DILocation(line: 76, column: 20, scope: !79)
!79 = distinct !DILexicalBlock(scope: !75, file: !1, line: 76, column: 5)
!80 = !DILocation(line: 76, column: 24, scope: !79)
!81 = !DILocation(line: 76, column: 22, scope: !79)
!82 = !DILocation(line: 76, column: 5, scope: !75)
!83 = !DILocation(line: 78, column: 16, scope: !84)
!84 = distinct !DILexicalBlock(scope: !79, file: !1, line: 77, column: 5)
!85 = !DILocation(line: 78, column: 20, scope: !84)
!86 = !DILocation(line: 78, column: 29, scope: !84)
!87 = !DILocation(line: 78, column: 35, scope: !84)
!88 = !DILocation(line: 78, column: 26, scope: !84)
!89 = !DILocation(line: 78, column: 13, scope: !84)
!90 = !DILocation(line: 79, column: 15, scope: !84)
!91 = !DILocation(line: 81, column: 9, scope: !84)
!92 = !DILocation(line: 82, column: 5, scope: !84)
!93 = !DILocation(line: 76, column: 34, scope: !79)
!94 = !DILocation(line: 76, column: 5, scope: !79)
!95 = distinct !{!95, !82, !96}
!96 = !DILocation(line: 82, column: 5, scope: !75)
!97 = !DILocation(line: 84, column: 12, scope: !63)
!98 = !DILocation(line: 84, column: 5, scope: !63)
!99 = distinct !DISubprogram(name: "Index_to_frequency", scope: !1, file: !1, line: 88, type: !100, isLocal: false, isDefinition: true, scopeLine: 89, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!100 = !DISubroutineType(types: !101)
!101 = !{!4, !13, !13}
!102 = !DILocalVariable(name: "NumSamples", arg: 1, scope: !99, file: !1, line: 88, type: !13)
!103 = !DILocation(line: 88, column: 38, scope: !99)
!104 = !DILocalVariable(name: "Index", arg: 2, scope: !99, file: !1, line: 88, type: !13)
!105 = !DILocation(line: 88, column: 59, scope: !99)
!106 = !DILocation(line: 90, column: 10, scope: !107)
!107 = distinct !DILexicalBlock(scope: !99, file: !1, line: 90, column: 10)
!108 = !DILocation(line: 90, column: 19, scope: !107)
!109 = !DILocation(line: 90, column: 16, scope: !107)
!110 = !DILocation(line: 90, column: 10, scope: !99)
!111 = !DILocation(line: 91, column: 9, scope: !107)
!112 = !DILocation(line: 92, column: 15, scope: !113)
!113 = distinct !DILexicalBlock(scope: !107, file: !1, line: 92, column: 15)
!114 = !DILocation(line: 92, column: 24, scope: !113)
!115 = !DILocation(line: 92, column: 34, scope: !113)
!116 = !DILocation(line: 92, column: 21, scope: !113)
!117 = !DILocation(line: 92, column: 15, scope: !107)
!118 = !DILocation(line: 93, column: 24, scope: !113)
!119 = !DILocation(line: 93, column: 16, scope: !113)
!120 = !DILocation(line: 93, column: 40, scope: !113)
!121 = !DILocation(line: 93, column: 32, scope: !113)
!122 = !DILocation(line: 93, column: 30, scope: !113)
!123 = !DILocation(line: 93, column: 9, scope: !113)
!124 = !DILocation(line: 95, column: 22, scope: !99)
!125 = !DILocation(line: 95, column: 33, scope: !99)
!126 = !DILocation(line: 95, column: 32, scope: !99)
!127 = !DILocation(line: 95, column: 13, scope: !99)
!128 = !DILocation(line: 95, column: 12, scope: !99)
!129 = !DILocation(line: 95, column: 50, scope: !99)
!130 = !DILocation(line: 95, column: 42, scope: !99)
!131 = !DILocation(line: 95, column: 40, scope: !99)
!132 = !DILocation(line: 95, column: 5, scope: !99)
!133 = !DILocation(line: 96, column: 1, scope: !99)
