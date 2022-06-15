; ModuleID = 'llvm-link'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@invfft = global i32 0, align 4, !dbg !0
@MAXWAVES = global i32 4, align 4, !dbg !6
@MAXSIZE = common global i32 0, align 4, !dbg !9
@realin = internal global [1024 x float] zeroinitializer, align 16, !dbg !11
@imagin = internal global [1024 x float] zeroinitializer, align 16, !dbg !17
@realout = internal global [1024 x float] zeroinitializer, align 16, !dbg !19
@imagout = internal global [1024 x float] zeroinitializer, align 16, !dbg !21
@Coeff = internal global [16 x float] zeroinitializer, align 16, !dbg !23
@Amp = internal global [16 x float] zeroinitializer, align 16, !dbg !28
@.str = private unnamed_addr constant [10 x i8] c"RealOut:\0A\00", align 1
@.str.1 = private unnamed_addr constant [5 x i8] c"%f \09\00", align 1
@.str.2 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@.str.3 = private unnamed_addr constant [10 x i8] c"ImagOut:\0A\00", align 1
@.str.4 = private unnamed_addr constant [7 x i8] c"RealIn\00", align 1
@.str.1.5 = private unnamed_addr constant [8 x i8] c"RealOut\00", align 1
@.str.2.6 = private unnamed_addr constant [8 x i8] c"ImagOut\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 !dbg !43 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 128, i32* @MAXSIZE, align 4, !dbg !46
  %2 = call i32 @old_main(), !dbg !47
  store i32 1, i32* @invfft, align 4, !dbg !48
  store i32 256, i32* @MAXSIZE, align 4, !dbg !49
  %3 = call i32 @old_main(), !dbg !50
  ret i32 0, !dbg !51
}

; Function Attrs: noinline nounwind optnone uwtable
define i32 @old_main() #0 !dbg !52 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca float*, align 8
  %4 = alloca float*, align 8
  %5 = alloca float*, align 8
  %6 = alloca float*, align 8
  %7 = alloca float*, align 8
  %8 = alloca float*, align 8
  call void @llvm.dbg.declare(metadata i32* %1, metadata !53, metadata !DIExpression()), !dbg !54
  call void @llvm.dbg.declare(metadata i32* %2, metadata !55, metadata !DIExpression()), !dbg !56
  call void @llvm.dbg.declare(metadata float** %3, metadata !57, metadata !DIExpression()), !dbg !59
  call void @llvm.dbg.declare(metadata float** %4, metadata !60, metadata !DIExpression()), !dbg !61
  call void @llvm.dbg.declare(metadata float** %5, metadata !62, metadata !DIExpression()), !dbg !63
  call void @llvm.dbg.declare(metadata float** %6, metadata !64, metadata !DIExpression()), !dbg !65
  call void @llvm.dbg.declare(metadata float** %7, metadata !66, metadata !DIExpression()), !dbg !67
  call void @llvm.dbg.declare(metadata float** %8, metadata !68, metadata !DIExpression()), !dbg !69
  call void @srand(i32 1) #5, !dbg !70
  store float* getelementptr inbounds ([1024 x float], [1024 x float]* @realin, i32 0, i32 0), float** %3, align 8, !dbg !71
  store float* getelementptr inbounds ([1024 x float], [1024 x float]* @imagin, i32 0, i32 0), float** %4, align 8, !dbg !72
  store float* getelementptr inbounds ([1024 x float], [1024 x float]* @realout, i32 0, i32 0), float** %5, align 8, !dbg !73
  store float* getelementptr inbounds ([1024 x float], [1024 x float]* @imagout, i32 0, i32 0), float** %6, align 8, !dbg !74
  store float* getelementptr inbounds ([16 x float], [16 x float]* @Coeff, i32 0, i32 0), float** %7, align 8, !dbg !75
  store float* getelementptr inbounds ([16 x float], [16 x float]* @Amp, i32 0, i32 0), float** %8, align 8, !dbg !76
  store i32 0, i32* %1, align 4, !dbg !77
  br label %9, !dbg !79

; <label>:9:                                      ; preds = %29, %0
  %10 = load i32, i32* %1, align 4, !dbg !80
  %11 = load i32, i32* @MAXWAVES, align 4, !dbg !82
  %12 = icmp ult i32 %10, %11, !dbg !83
  br i1 %12, label %13, label %32, !dbg !84

; <label>:13:                                     ; preds = %9
  %14 = call i32 @rand() #5, !dbg !85
  %15 = srem i32 %14, 1000, !dbg !87
  %16 = sitofp i32 %15 to float, !dbg !85
  %17 = load float*, float** %7, align 8, !dbg !88
  %18 = load i32, i32* %1, align 4, !dbg !89
  %19 = zext i32 %18 to i64, !dbg !88
  %20 = getelementptr inbounds float, float* %17, i64 %19, !dbg !88
  store float %16, float* %20, align 4, !dbg !90
  %21 = call i32 @rand() #5, !dbg !91
  %22 = srem i32 %21, 1000, !dbg !92
  %23 = sitofp i32 %22 to float, !dbg !91
  %24 = load float*, float** %8, align 8, !dbg !93
  %25 = load i32, i32* %1, align 4, !dbg !94
  %26 = zext i32 %25 to i64, !dbg !93
  %27 = getelementptr inbounds float, float* %24, i64 %26, !dbg !93
  store float %23, float* %27, align 4, !dbg !95
  %28 = call i32 (...) @checkpoint(), !dbg !96
  br label %29, !dbg !97

; <label>:29:                                     ; preds = %13
  %30 = load i32, i32* %1, align 4, !dbg !98
  %31 = add i32 %30, 1, !dbg !98
  store i32 %31, i32* %1, align 4, !dbg !98
  br label %9, !dbg !99, !llvm.loop !100

; <label>:32:                                     ; preds = %9
  store i32 0, i32* %1, align 4, !dbg !102
  br label %33, !dbg !104

; <label>:33:                                     ; preds = %113, %32
  %34 = load i32, i32* %1, align 4, !dbg !105
  %35 = load i32, i32* @MAXSIZE, align 4, !dbg !107
  %36 = icmp ult i32 %34, %35, !dbg !108
  br i1 %36, label %37, label %116, !dbg !109

; <label>:37:                                     ; preds = %33
  %38 = load float*, float** %3, align 8, !dbg !110
  %39 = load i32, i32* %1, align 4, !dbg !112
  %40 = zext i32 %39 to i64, !dbg !110
  %41 = getelementptr inbounds float, float* %38, i64 %40, !dbg !110
  store float 0.000000e+00, float* %41, align 4, !dbg !113
  store i32 0, i32* %2, align 4, !dbg !114
  br label %42, !dbg !116

; <label>:42:                                     ; preds = %108, %37
  %43 = load i32, i32* %2, align 4, !dbg !117
  %44 = load i32, i32* @MAXWAVES, align 4, !dbg !119
  %45 = icmp ult i32 %43, %44, !dbg !120
  br i1 %45, label %46, label %111, !dbg !121

; <label>:46:                                     ; preds = %42
  %47 = call i32 @rand() #5, !dbg !122
  %48 = srem i32 %47, 2, !dbg !125
  %49 = icmp ne i32 %48, 0, !dbg !125
  br i1 %49, label %50, label %76, !dbg !126

; <label>:50:                                     ; preds = %46
  %51 = load float*, float** %7, align 8, !dbg !127
  %52 = load i32, i32* %2, align 4, !dbg !129
  %53 = zext i32 %52 to i64, !dbg !127
  %54 = getelementptr inbounds float, float* %51, i64 %53, !dbg !127
  %55 = load float, float* %54, align 4, !dbg !127
  %56 = fpext float %55 to double, !dbg !127
  %57 = load float*, float** %8, align 8, !dbg !130
  %58 = load i32, i32* %2, align 4, !dbg !131
  %59 = zext i32 %58 to i64, !dbg !130
  %60 = getelementptr inbounds float, float* %57, i64 %59, !dbg !130
  %61 = load float, float* %60, align 4, !dbg !130
  %62 = load i32, i32* %1, align 4, !dbg !132
  %63 = uitofp i32 %62 to float, !dbg !132
  %64 = fmul float %61, %63, !dbg !133
  %65 = fpext float %64 to double, !dbg !130
  %66 = call double @cos(double %65) #5, !dbg !134
  %67 = fmul double %56, %66, !dbg !135
  %68 = load float*, float** %3, align 8, !dbg !136
  %69 = load i32, i32* %1, align 4, !dbg !137
  %70 = zext i32 %69 to i64, !dbg !136
  %71 = getelementptr inbounds float, float* %68, i64 %70, !dbg !136
  %72 = load float, float* %71, align 4, !dbg !138
  %73 = fpext float %72 to double, !dbg !138
  %74 = fadd double %73, %67, !dbg !138
  %75 = fptrunc double %74 to float, !dbg !138
  store float %75, float* %71, align 4, !dbg !138
  br label %102, !dbg !139

; <label>:76:                                     ; preds = %46
  %77 = load float*, float** %7, align 8, !dbg !140
  %78 = load i32, i32* %2, align 4, !dbg !142
  %79 = zext i32 %78 to i64, !dbg !140
  %80 = getelementptr inbounds float, float* %77, i64 %79, !dbg !140
  %81 = load float, float* %80, align 4, !dbg !140
  %82 = fpext float %81 to double, !dbg !140
  %83 = load float*, float** %8, align 8, !dbg !143
  %84 = load i32, i32* %2, align 4, !dbg !144
  %85 = zext i32 %84 to i64, !dbg !143
  %86 = getelementptr inbounds float, float* %83, i64 %85, !dbg !143
  %87 = load float, float* %86, align 4, !dbg !143
  %88 = load i32, i32* %1, align 4, !dbg !145
  %89 = uitofp i32 %88 to float, !dbg !145
  %90 = fmul float %87, %89, !dbg !146
  %91 = fpext float %90 to double, !dbg !143
  %92 = call double @sin(double %91) #5, !dbg !147
  %93 = fmul double %82, %92, !dbg !148
  %94 = load float*, float** %3, align 8, !dbg !149
  %95 = load i32, i32* %1, align 4, !dbg !150
  %96 = zext i32 %95 to i64, !dbg !149
  %97 = getelementptr inbounds float, float* %94, i64 %96, !dbg !149
  %98 = load float, float* %97, align 4, !dbg !151
  %99 = fpext float %98 to double, !dbg !151
  %100 = fadd double %99, %93, !dbg !151
  %101 = fptrunc double %100 to float, !dbg !151
  store float %101, float* %97, align 4, !dbg !151
  br label %102

; <label>:102:                                    ; preds = %76, %50
  %103 = load float*, float** %4, align 8, !dbg !152
  %104 = load i32, i32* %1, align 4, !dbg !153
  %105 = zext i32 %104 to i64, !dbg !152
  %106 = getelementptr inbounds float, float* %103, i64 %105, !dbg !152
  store float 0.000000e+00, float* %106, align 4, !dbg !154
  %107 = call i32 (...) @checkpoint(), !dbg !155
  br label %108, !dbg !156

; <label>:108:                                    ; preds = %102
  %109 = load i32, i32* %2, align 4, !dbg !157
  %110 = add i32 %109, 1, !dbg !157
  store i32 %110, i32* %2, align 4, !dbg !157
  br label %42, !dbg !158, !llvm.loop !159

; <label>:111:                                    ; preds = %42
  %112 = call i32 (...) @checkpoint(), !dbg !161
  br label %113, !dbg !162

; <label>:113:                                    ; preds = %111
  %114 = load i32, i32* %1, align 4, !dbg !163
  %115 = add i32 %114, 1, !dbg !163
  store i32 %115, i32* %1, align 4, !dbg !163
  br label %33, !dbg !164, !llvm.loop !165

; <label>:116:                                    ; preds = %33
  %117 = load i32, i32* @MAXSIZE, align 4, !dbg !167
  %118 = load i32, i32* @invfft, align 4, !dbg !168
  %119 = load float*, float** %3, align 8, !dbg !169
  %120 = load float*, float** %4, align 8, !dbg !170
  %121 = load float*, float** %5, align 8, !dbg !171
  %122 = load float*, float** %6, align 8, !dbg !172
  call void @fft_float(i32 %117, i32 %118, float* %119, float* %120, float* %121, float* %122), !dbg !173
  %123 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str, i32 0, i32 0)), !dbg !174
  store i32 0, i32* %1, align 4, !dbg !175
  br label %124, !dbg !177

; <label>:124:                                    ; preds = %137, %116
  %125 = load i32, i32* %1, align 4, !dbg !178
  %126 = load i32, i32* @MAXSIZE, align 4, !dbg !180
  %127 = icmp ult i32 %125, %126, !dbg !181
  br i1 %127, label %128, label %140, !dbg !182

; <label>:128:                                    ; preds = %124
  %129 = load float*, float** %5, align 8, !dbg !183
  %130 = load i32, i32* %1, align 4, !dbg !185
  %131 = zext i32 %130 to i64, !dbg !183
  %132 = getelementptr inbounds float, float* %129, i64 %131, !dbg !183
  %133 = load float, float* %132, align 4, !dbg !183
  %134 = fpext float %133 to double, !dbg !183
  %135 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i32 0, i32 0), double %134), !dbg !186
  %136 = call i32 (...) @checkpoint(), !dbg !187
  br label %137, !dbg !188

; <label>:137:                                    ; preds = %128
  %138 = load i32, i32* %1, align 4, !dbg !189
  %139 = add i32 %138, 1, !dbg !189
  store i32 %139, i32* %1, align 4, !dbg !189
  br label %124, !dbg !190, !llvm.loop !191

; <label>:140:                                    ; preds = %124
  %141 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2, i32 0, i32 0)), !dbg !193
  %142 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str.3, i32 0, i32 0)), !dbg !194
  store i32 0, i32* %1, align 4, !dbg !195
  br label %143, !dbg !197

; <label>:143:                                    ; preds = %156, %140
  %144 = load i32, i32* %1, align 4, !dbg !198
  %145 = load i32, i32* @MAXSIZE, align 4, !dbg !200
  %146 = icmp ult i32 %144, %145, !dbg !201
  br i1 %146, label %147, label %159, !dbg !202

; <label>:147:                                    ; preds = %143
  %148 = load float*, float** %6, align 8, !dbg !203
  %149 = load i32, i32* %1, align 4, !dbg !205
  %150 = zext i32 %149 to i64, !dbg !203
  %151 = getelementptr inbounds float, float* %148, i64 %150, !dbg !203
  %152 = load float, float* %151, align 4, !dbg !203
  %153 = fpext float %152 to double, !dbg !203
  %154 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i32 0, i32 0), double %153), !dbg !206
  %155 = call i32 (...) @checkpoint(), !dbg !207
  br label %156, !dbg !208

; <label>:156:                                    ; preds = %147
  %157 = load i32, i32* %1, align 4, !dbg !209
  %158 = add i32 %157, 1, !dbg !209
  store i32 %158, i32* %1, align 4, !dbg !209
  br label %143, !dbg !210, !llvm.loop !211

; <label>:159:                                    ; preds = %143
  %160 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str.2, i32 0, i32 0)), !dbg !213
  ret i32 0, !dbg !214
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: nounwind
declare void @srand(i32) #2

; Function Attrs: nounwind
declare i32 @rand() #2

declare i32 @checkpoint(...) #3

; Function Attrs: nounwind
declare double @cos(double) #2

; Function Attrs: nounwind
declare double @sin(double) #2

declare i32 @printf(i8*, ...) #3

; Function Attrs: noinline nounwind optnone uwtable
define i32 @IsPowerOfTwo(i32) #0 !dbg !215 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !218, metadata !DIExpression()), !dbg !219
  %4 = load i32, i32* %3, align 4, !dbg !220
  %5 = icmp ult i32 %4, 2, !dbg !222
  br i1 %5, label %6, label %7, !dbg !223

; <label>:6:                                      ; preds = %1
  store i32 0, i32* %2, align 4, !dbg !224
  br label %15, !dbg !224

; <label>:7:                                      ; preds = %1
  %8 = load i32, i32* %3, align 4, !dbg !225
  %9 = load i32, i32* %3, align 4, !dbg !227
  %10 = sub i32 %9, 1, !dbg !228
  %11 = and i32 %8, %10, !dbg !229
  %12 = icmp ne i32 %11, 0, !dbg !229
  br i1 %12, label %13, label %14, !dbg !230

; <label>:13:                                     ; preds = %7
  store i32 0, i32* %2, align 4, !dbg !231
  br label %15, !dbg !231

; <label>:14:                                     ; preds = %7
  store i32 1, i32* %2, align 4, !dbg !232
  br label %15, !dbg !232

; <label>:15:                                     ; preds = %14, %13, %6
  %16 = load i32, i32* %2, align 4, !dbg !233
  ret i32 %16, !dbg !233
}

; Function Attrs: noinline nounwind optnone uwtable
define i32 @NumberOfBitsNeeded(i32) #0 !dbg !234 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  call void @llvm.dbg.declare(metadata i32* %2, metadata !237, metadata !DIExpression()), !dbg !238
  call void @llvm.dbg.declare(metadata i32* %3, metadata !239, metadata !DIExpression()), !dbg !240
  %4 = load i32, i32* %2, align 4, !dbg !241
  %5 = icmp ult i32 %4, 2, !dbg !243
  br i1 %5, label %6, label %7, !dbg !244

; <label>:6:                                      ; preds = %1
  call void @exit(i32 1) #6, !dbg !245
  unreachable, !dbg !245

; <label>:7:                                      ; preds = %1
  store i32 0, i32* %3, align 4, !dbg !247
  br label %8, !dbg !249

; <label>:8:                                      ; preds = %18, %7
  %9 = load i32, i32* %2, align 4, !dbg !250
  %10 = load i32, i32* %3, align 4, !dbg !254
  %11 = shl i32 1, %10, !dbg !255
  %12 = and i32 %9, %11, !dbg !256
  %13 = icmp ne i32 %12, 0, !dbg !256
  br i1 %13, label %14, label %16, !dbg !257

; <label>:14:                                     ; preds = %8
  %15 = load i32, i32* %3, align 4, !dbg !258
  ret i32 %15, !dbg !259

; <label>:16:                                     ; preds = %8
  %17 = call i32 (...) @checkpoint(), !dbg !260
  br label %18, !dbg !261

; <label>:18:                                     ; preds = %16
  %19 = load i32, i32* %3, align 4, !dbg !262
  %20 = add i32 %19, 1, !dbg !262
  store i32 %20, i32* %3, align 4, !dbg !262
  br label %8, !dbg !263, !llvm.loop !264
}

; Function Attrs: noreturn nounwind
declare void @exit(i32) #4

; Function Attrs: noinline nounwind optnone uwtable
define i32 @ReverseBits(i32, i32) #0 !dbg !267 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !270, metadata !DIExpression()), !dbg !271
  store i32 %1, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !272, metadata !DIExpression()), !dbg !273
  call void @llvm.dbg.declare(metadata i32* %5, metadata !274, metadata !DIExpression()), !dbg !275
  call void @llvm.dbg.declare(metadata i32* %6, metadata !276, metadata !DIExpression()), !dbg !277
  store i32 0, i32* %6, align 4, !dbg !278
  store i32 0, i32* %5, align 4, !dbg !280
  br label %7, !dbg !281

; <label>:7:                                      ; preds = %20, %2
  %8 = load i32, i32* %5, align 4, !dbg !282
  %9 = load i32, i32* %4, align 4, !dbg !284
  %10 = icmp ult i32 %8, %9, !dbg !285
  br i1 %10, label %11, label %23, !dbg !286

; <label>:11:                                     ; preds = %7
  %12 = load i32, i32* %6, align 4, !dbg !287
  %13 = shl i32 %12, 1, !dbg !289
  %14 = load i32, i32* %3, align 4, !dbg !290
  %15 = and i32 %14, 1, !dbg !291
  %16 = or i32 %13, %15, !dbg !292
  store i32 %16, i32* %6, align 4, !dbg !293
  %17 = load i32, i32* %3, align 4, !dbg !294
  %18 = lshr i32 %17, 1, !dbg !294
  store i32 %18, i32* %3, align 4, !dbg !294
  %19 = call i32 (...) @checkpoint(), !dbg !295
  br label %20, !dbg !296

; <label>:20:                                     ; preds = %11
  %21 = load i32, i32* %5, align 4, !dbg !297
  %22 = add i32 %21, 1, !dbg !297
  store i32 %22, i32* %5, align 4, !dbg !297
  br label %7, !dbg !298, !llvm.loop !299

; <label>:23:                                     ; preds = %7
  %24 = load i32, i32* %6, align 4, !dbg !301
  ret i32 %24, !dbg !302
}

; Function Attrs: noinline nounwind optnone uwtable
define double @Index_to_frequency(i32, i32) #0 !dbg !303 {
  %3 = alloca double, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !306, metadata !DIExpression()), !dbg !307
  store i32 %1, i32* %5, align 4
  call void @llvm.dbg.declare(metadata i32* %5, metadata !308, metadata !DIExpression()), !dbg !309
  %6 = load i32, i32* %5, align 4, !dbg !310
  %7 = load i32, i32* %4, align 4, !dbg !312
  %8 = icmp uge i32 %6, %7, !dbg !313
  br i1 %8, label %9, label %10, !dbg !314

; <label>:9:                                      ; preds = %2
  store double 0.000000e+00, double* %3, align 8, !dbg !315
  br label %31, !dbg !315

; <label>:10:                                     ; preds = %2
  %11 = load i32, i32* %5, align 4, !dbg !316
  %12 = load i32, i32* %4, align 4, !dbg !318
  %13 = udiv i32 %12, 2, !dbg !319
  %14 = icmp ule i32 %11, %13, !dbg !320
  br i1 %14, label %15, label %21, !dbg !321

; <label>:15:                                     ; preds = %10
  %16 = load i32, i32* %5, align 4, !dbg !322
  %17 = uitofp i32 %16 to double, !dbg !323
  %18 = load i32, i32* %4, align 4, !dbg !324
  %19 = uitofp i32 %18 to double, !dbg !325
  %20 = fdiv double %17, %19, !dbg !326
  store double %20, double* %3, align 8, !dbg !327
  br label %31, !dbg !327

; <label>:21:                                     ; preds = %10
  br label %22

; <label>:22:                                     ; preds = %21
  %23 = load i32, i32* %4, align 4, !dbg !328
  %24 = load i32, i32* %5, align 4, !dbg !329
  %25 = sub i32 %23, %24, !dbg !330
  %26 = uitofp i32 %25 to double, !dbg !331
  %27 = fsub double -0.000000e+00, %26, !dbg !332
  %28 = load i32, i32* %4, align 4, !dbg !333
  %29 = uitofp i32 %28 to double, !dbg !334
  %30 = fdiv double %27, %29, !dbg !335
  store double %30, double* %3, align 8, !dbg !336
  br label %31, !dbg !336

; <label>:31:                                     ; preds = %22, %15, %9
  %32 = load double, double* %3, align 8, !dbg !337
  ret double %32, !dbg !337
}

; Function Attrs: noinline nounwind optnone uwtable
define void @fft_float(i32, i32, float*, float*, float*, float*) #0 !dbg !338 {
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca float*, align 8
  %10 = alloca float*, align 8
  %11 = alloca float*, align 8
  %12 = alloca float*, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  %18 = alloca i32, align 4
  %19 = alloca i32, align 4
  %20 = alloca double, align 8
  %21 = alloca double, align 8
  %22 = alloca double, align 8
  %23 = alloca double, align 8
  %24 = alloca double, align 8
  %25 = alloca double, align 8
  %26 = alloca double, align 8
  %27 = alloca double, align 8
  %28 = alloca double, align 8
  %29 = alloca [3 x double], align 16
  %30 = alloca [3 x double], align 16
  %31 = alloca double, align 8
  store i32 %0, i32* %7, align 4
  call void @llvm.dbg.declare(metadata i32* %7, metadata !341, metadata !DIExpression()), !dbg !342
  store i32 %1, i32* %8, align 4
  call void @llvm.dbg.declare(metadata i32* %8, metadata !343, metadata !DIExpression()), !dbg !344
  store float* %2, float** %9, align 8
  call void @llvm.dbg.declare(metadata float** %9, metadata !345, metadata !DIExpression()), !dbg !346
  store float* %3, float** %10, align 8
  call void @llvm.dbg.declare(metadata float** %10, metadata !347, metadata !DIExpression()), !dbg !348
  store float* %4, float** %11, align 8
  call void @llvm.dbg.declare(metadata float** %11, metadata !349, metadata !DIExpression()), !dbg !350
  store float* %5, float** %12, align 8
  call void @llvm.dbg.declare(metadata float** %12, metadata !351, metadata !DIExpression()), !dbg !352
  call void @llvm.dbg.declare(metadata i32* %13, metadata !353, metadata !DIExpression()), !dbg !354
  call void @llvm.dbg.declare(metadata i32* %14, metadata !355, metadata !DIExpression()), !dbg !356
  call void @llvm.dbg.declare(metadata i32* %15, metadata !357, metadata !DIExpression()), !dbg !358
  call void @llvm.dbg.declare(metadata i32* %16, metadata !359, metadata !DIExpression()), !dbg !360
  call void @llvm.dbg.declare(metadata i32* %17, metadata !361, metadata !DIExpression()), !dbg !362
  call void @llvm.dbg.declare(metadata i32* %18, metadata !363, metadata !DIExpression()), !dbg !364
  call void @llvm.dbg.declare(metadata i32* %19, metadata !365, metadata !DIExpression()), !dbg !366
  call void @llvm.dbg.declare(metadata double* %20, metadata !367, metadata !DIExpression()), !dbg !368
  store double 0x401921FB54442D18, double* %20, align 8, !dbg !368
  call void @llvm.dbg.declare(metadata double* %21, metadata !369, metadata !DIExpression()), !dbg !370
  call void @llvm.dbg.declare(metadata double* %22, metadata !371, metadata !DIExpression()), !dbg !372
  %32 = load i32, i32* %7, align 4, !dbg !373
  %33 = call i32 @IsPowerOfTwo(i32 %32), !dbg !375
  %34 = icmp ne i32 %33, 0, !dbg !375
  br i1 %34, label %36, label %35, !dbg !376

; <label>:35:                                     ; preds = %6
  call void @exit(i32 1) #6, !dbg !377
  unreachable, !dbg !377

; <label>:36:                                     ; preds = %6
  %37 = load i32, i32* %8, align 4, !dbg !379
  %38 = icmp ne i32 %37, 0, !dbg !379
  br i1 %38, label %39, label %42, !dbg !381

; <label>:39:                                     ; preds = %36
  %40 = load double, double* %20, align 8, !dbg !382
  %41 = fsub double -0.000000e+00, %40, !dbg !383
  store double %41, double* %20, align 8, !dbg !384
  br label %42, !dbg !385

; <label>:42:                                     ; preds = %39, %36
  %43 = load float*, float** %9, align 8, !dbg !386
  %44 = bitcast float* %43 to i8*, !dbg !386
  call void @CheckPointer(i8* %44, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.4, i32 0, i32 0)), !dbg !386
  %45 = load float*, float** %11, align 8, !dbg !387
  %46 = bitcast float* %45 to i8*, !dbg !387
  call void @CheckPointer(i8* %46, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.1.5, i32 0, i32 0)), !dbg !387
  %47 = load float*, float** %12, align 8, !dbg !388
  %48 = bitcast float* %47 to i8*, !dbg !388
  call void @CheckPointer(i8* %48, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.2.6, i32 0, i32 0)), !dbg !388
  %49 = load i32, i32* %7, align 4, !dbg !389
  %50 = call i32 @NumberOfBitsNeeded(i32 %49), !dbg !390
  store i32 %50, i32* %13, align 4, !dbg !391
  store i32 0, i32* %14, align 4, !dbg !392
  br label %51, !dbg !394

; <label>:51:                                     ; preds = %86, %42
  %52 = load i32, i32* %14, align 4, !dbg !395
  %53 = load i32, i32* %7, align 4, !dbg !397
  %54 = icmp ult i32 %52, %53, !dbg !398
  br i1 %54, label %55, label %89, !dbg !399

; <label>:55:                                     ; preds = %51
  %56 = load i32, i32* %14, align 4, !dbg !400
  %57 = load i32, i32* %13, align 4, !dbg !402
  %58 = call i32 @ReverseBits(i32 %56, i32 %57), !dbg !403
  store i32 %58, i32* %15, align 4, !dbg !404
  %59 = load float*, float** %9, align 8, !dbg !405
  %60 = load i32, i32* %14, align 4, !dbg !406
  %61 = zext i32 %60 to i64, !dbg !405
  %62 = getelementptr inbounds float, float* %59, i64 %61, !dbg !405
  %63 = load float, float* %62, align 4, !dbg !405
  %64 = load float*, float** %11, align 8, !dbg !407
  %65 = load i32, i32* %15, align 4, !dbg !408
  %66 = zext i32 %65 to i64, !dbg !407
  %67 = getelementptr inbounds float, float* %64, i64 %66, !dbg !407
  store float %63, float* %67, align 4, !dbg !409
  %68 = load float*, float** %10, align 8, !dbg !410
  %69 = icmp eq float* %68, null, !dbg !411
  br i1 %69, label %70, label %71, !dbg !412

; <label>:70:                                     ; preds = %55
  br label %78, !dbg !412

; <label>:71:                                     ; preds = %55
  %72 = load float*, float** %10, align 8, !dbg !413
  %73 = load i32, i32* %14, align 4, !dbg !414
  %74 = zext i32 %73 to i64, !dbg !413
  %75 = getelementptr inbounds float, float* %72, i64 %74, !dbg !413
  %76 = load float, float* %75, align 4, !dbg !413
  %77 = fpext float %76 to double, !dbg !413
  br label %78, !dbg !412

; <label>:78:                                     ; preds = %71, %70
  %79 = phi double [ 0.000000e+00, %70 ], [ %77, %71 ], !dbg !412
  %80 = fptrunc double %79 to float, !dbg !412
  %81 = load float*, float** %12, align 8, !dbg !415
  %82 = load i32, i32* %15, align 4, !dbg !416
  %83 = zext i32 %82 to i64, !dbg !415
  %84 = getelementptr inbounds float, float* %81, i64 %83, !dbg !415
  store float %80, float* %84, align 4, !dbg !417
  %85 = call i32 (...) @checkpoint(), !dbg !418
  br label %86, !dbg !419

; <label>:86:                                     ; preds = %78
  %87 = load i32, i32* %14, align 4, !dbg !420
  %88 = add i32 %87, 1, !dbg !420
  store i32 %88, i32* %14, align 4, !dbg !420
  br label %51, !dbg !421, !llvm.loop !422

; <label>:89:                                     ; preds = %51
  store i32 1, i32* %19, align 4, !dbg !424
  store i32 2, i32* %18, align 4, !dbg !425
  br label %90, !dbg !427

; <label>:90:                                     ; preds = %260, %89
  %91 = load i32, i32* %18, align 4, !dbg !428
  %92 = load i32, i32* %7, align 4, !dbg !430
  %93 = icmp ule i32 %91, %92, !dbg !431
  br i1 %93, label %94, label %263, !dbg !432

; <label>:94:                                     ; preds = %90
  call void @llvm.dbg.declare(metadata double* %23, metadata !433, metadata !DIExpression()), !dbg !435
  %95 = load double, double* %20, align 8, !dbg !436
  %96 = load i32, i32* %18, align 4, !dbg !437
  %97 = uitofp i32 %96 to double, !dbg !438
  %98 = fdiv double %95, %97, !dbg !439
  store double %98, double* %23, align 8, !dbg !435
  call void @llvm.dbg.declare(metadata double* %24, metadata !440, metadata !DIExpression()), !dbg !441
  %99 = load double, double* %23, align 8, !dbg !442
  %100 = fmul double -2.000000e+00, %99, !dbg !443
  %101 = call double @sin(double %100) #5, !dbg !444
  store double %101, double* %24, align 8, !dbg !441
  call void @llvm.dbg.declare(metadata double* %25, metadata !445, metadata !DIExpression()), !dbg !446
  %102 = load double, double* %23, align 8, !dbg !447
  %103 = fsub double -0.000000e+00, %102, !dbg !448
  %104 = call double @sin(double %103) #5, !dbg !449
  store double %104, double* %25, align 8, !dbg !446
  call void @llvm.dbg.declare(metadata double* %26, metadata !450, metadata !DIExpression()), !dbg !451
  %105 = load double, double* %23, align 8, !dbg !452
  %106 = fmul double -2.000000e+00, %105, !dbg !453
  %107 = call double @cos(double %106) #5, !dbg !454
  store double %107, double* %26, align 8, !dbg !451
  call void @llvm.dbg.declare(metadata double* %27, metadata !455, metadata !DIExpression()), !dbg !456
  %108 = load double, double* %23, align 8, !dbg !457
  %109 = fsub double -0.000000e+00, %108, !dbg !458
  %110 = call double @cos(double %109) #5, !dbg !459
  store double %110, double* %27, align 8, !dbg !456
  call void @llvm.dbg.declare(metadata double* %28, metadata !460, metadata !DIExpression()), !dbg !461
  %111 = load double, double* %27, align 8, !dbg !462
  %112 = fmul double 2.000000e+00, %111, !dbg !463
  store double %112, double* %28, align 8, !dbg !461
  call void @llvm.dbg.declare(metadata [3 x double]* %29, metadata !464, metadata !DIExpression()), !dbg !468
  call void @llvm.dbg.declare(metadata [3 x double]* %30, metadata !469, metadata !DIExpression()), !dbg !470
  store i32 0, i32* %14, align 4, !dbg !471
  br label %113, !dbg !473

; <label>:113:                                    ; preds = %253, %94
  %114 = load i32, i32* %14, align 4, !dbg !474
  %115 = load i32, i32* %7, align 4, !dbg !476
  %116 = icmp ult i32 %114, %115, !dbg !477
  br i1 %116, label %117, label %257, !dbg !478

; <label>:117:                                    ; preds = %113
  %118 = load double, double* %26, align 8, !dbg !479
  %119 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 2, !dbg !481
  store double %118, double* %119, align 16, !dbg !482
  %120 = load double, double* %27, align 8, !dbg !483
  %121 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !484
  store double %120, double* %121, align 8, !dbg !485
  %122 = load double, double* %24, align 8, !dbg !486
  %123 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 2, !dbg !487
  store double %122, double* %123, align 16, !dbg !488
  %124 = load double, double* %25, align 8, !dbg !489
  %125 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !490
  store double %124, double* %125, align 8, !dbg !491
  %126 = load i32, i32* %14, align 4, !dbg !492
  store i32 %126, i32* %15, align 4, !dbg !494
  store i32 0, i32* %17, align 4, !dbg !495
  br label %127, !dbg !496

; <label>:127:                                    ; preds = %246, %117
  %128 = load i32, i32* %17, align 4, !dbg !497
  %129 = load i32, i32* %19, align 4, !dbg !499
  %130 = icmp ult i32 %128, %129, !dbg !500
  br i1 %130, label %131, label %251, !dbg !501

; <label>:131:                                    ; preds = %127
  %132 = load double, double* %28, align 8, !dbg !502
  %133 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !504
  %134 = load double, double* %133, align 8, !dbg !504
  %135 = fmul double %132, %134, !dbg !505
  %136 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 2, !dbg !506
  %137 = load double, double* %136, align 16, !dbg !506
  %138 = fsub double %135, %137, !dbg !507
  %139 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !508
  store double %138, double* %139, align 16, !dbg !509
  %140 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !510
  %141 = load double, double* %140, align 8, !dbg !510
  %142 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 2, !dbg !511
  store double %141, double* %142, align 16, !dbg !512
  %143 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !513
  %144 = load double, double* %143, align 16, !dbg !513
  %145 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !514
  store double %144, double* %145, align 8, !dbg !515
  %146 = load double, double* %28, align 8, !dbg !516
  %147 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !517
  %148 = load double, double* %147, align 8, !dbg !517
  %149 = fmul double %146, %148, !dbg !518
  %150 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 2, !dbg !519
  %151 = load double, double* %150, align 16, !dbg !519
  %152 = fsub double %149, %151, !dbg !520
  %153 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !521
  store double %152, double* %153, align 16, !dbg !522
  %154 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !523
  %155 = load double, double* %154, align 8, !dbg !523
  %156 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 2, !dbg !524
  store double %155, double* %156, align 16, !dbg !525
  %157 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !526
  %158 = load double, double* %157, align 16, !dbg !526
  %159 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !527
  store double %158, double* %159, align 8, !dbg !528
  %160 = load i32, i32* %15, align 4, !dbg !529
  %161 = load i32, i32* %19, align 4, !dbg !530
  %162 = add i32 %160, %161, !dbg !531
  store i32 %162, i32* %16, align 4, !dbg !532
  %163 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !533
  %164 = load double, double* %163, align 16, !dbg !533
  %165 = load float*, float** %11, align 8, !dbg !534
  %166 = load i32, i32* %16, align 4, !dbg !535
  %167 = zext i32 %166 to i64, !dbg !534
  %168 = getelementptr inbounds float, float* %165, i64 %167, !dbg !534
  %169 = load float, float* %168, align 4, !dbg !534
  %170 = fpext float %169 to double, !dbg !534
  %171 = fmul double %164, %170, !dbg !536
  %172 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !537
  %173 = load double, double* %172, align 16, !dbg !537
  %174 = load float*, float** %12, align 8, !dbg !538
  %175 = load i32, i32* %16, align 4, !dbg !539
  %176 = zext i32 %175 to i64, !dbg !538
  %177 = getelementptr inbounds float, float* %174, i64 %176, !dbg !538
  %178 = load float, float* %177, align 4, !dbg !538
  %179 = fpext float %178 to double, !dbg !538
  %180 = fmul double %173, %179, !dbg !540
  %181 = fsub double %171, %180, !dbg !541
  store double %181, double* %21, align 8, !dbg !542
  %182 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !543
  %183 = load double, double* %182, align 16, !dbg !543
  %184 = load float*, float** %12, align 8, !dbg !544
  %185 = load i32, i32* %16, align 4, !dbg !545
  %186 = zext i32 %185 to i64, !dbg !544
  %187 = getelementptr inbounds float, float* %184, i64 %186, !dbg !544
  %188 = load float, float* %187, align 4, !dbg !544
  %189 = fpext float %188 to double, !dbg !544
  %190 = fmul double %183, %189, !dbg !546
  %191 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !547
  %192 = load double, double* %191, align 16, !dbg !547
  %193 = load float*, float** %11, align 8, !dbg !548
  %194 = load i32, i32* %16, align 4, !dbg !549
  %195 = zext i32 %194 to i64, !dbg !548
  %196 = getelementptr inbounds float, float* %193, i64 %195, !dbg !548
  %197 = load float, float* %196, align 4, !dbg !548
  %198 = fpext float %197 to double, !dbg !548
  %199 = fmul double %192, %198, !dbg !550
  %200 = fadd double %190, %199, !dbg !551
  store double %200, double* %22, align 8, !dbg !552
  %201 = load float*, float** %11, align 8, !dbg !553
  %202 = load i32, i32* %15, align 4, !dbg !554
  %203 = zext i32 %202 to i64, !dbg !553
  %204 = getelementptr inbounds float, float* %201, i64 %203, !dbg !553
  %205 = load float, float* %204, align 4, !dbg !553
  %206 = fpext float %205 to double, !dbg !553
  %207 = load double, double* %21, align 8, !dbg !555
  %208 = fsub double %206, %207, !dbg !556
  %209 = fptrunc double %208 to float, !dbg !553
  %210 = load float*, float** %11, align 8, !dbg !557
  %211 = load i32, i32* %16, align 4, !dbg !558
  %212 = zext i32 %211 to i64, !dbg !557
  %213 = getelementptr inbounds float, float* %210, i64 %212, !dbg !557
  store float %209, float* %213, align 4, !dbg !559
  %214 = load float*, float** %12, align 8, !dbg !560
  %215 = load i32, i32* %15, align 4, !dbg !561
  %216 = zext i32 %215 to i64, !dbg !560
  %217 = getelementptr inbounds float, float* %214, i64 %216, !dbg !560
  %218 = load float, float* %217, align 4, !dbg !560
  %219 = fpext float %218 to double, !dbg !560
  %220 = load double, double* %22, align 8, !dbg !562
  %221 = fsub double %219, %220, !dbg !563
  %222 = fptrunc double %221 to float, !dbg !560
  %223 = load float*, float** %12, align 8, !dbg !564
  %224 = load i32, i32* %16, align 4, !dbg !565
  %225 = zext i32 %224 to i64, !dbg !564
  %226 = getelementptr inbounds float, float* %223, i64 %225, !dbg !564
  store float %222, float* %226, align 4, !dbg !566
  %227 = load double, double* %21, align 8, !dbg !567
  %228 = load float*, float** %11, align 8, !dbg !568
  %229 = load i32, i32* %15, align 4, !dbg !569
  %230 = zext i32 %229 to i64, !dbg !568
  %231 = getelementptr inbounds float, float* %228, i64 %230, !dbg !568
  %232 = load float, float* %231, align 4, !dbg !570
  %233 = fpext float %232 to double, !dbg !570
  %234 = fadd double %233, %227, !dbg !570
  %235 = fptrunc double %234 to float, !dbg !570
  store float %235, float* %231, align 4, !dbg !570
  %236 = load double, double* %22, align 8, !dbg !571
  %237 = load float*, float** %12, align 8, !dbg !572
  %238 = load i32, i32* %15, align 4, !dbg !573
  %239 = zext i32 %238 to i64, !dbg !572
  %240 = getelementptr inbounds float, float* %237, i64 %239, !dbg !572
  %241 = load float, float* %240, align 4, !dbg !574
  %242 = fpext float %241 to double, !dbg !574
  %243 = fadd double %242, %236, !dbg !574
  %244 = fptrunc double %243 to float, !dbg !574
  store float %244, float* %240, align 4, !dbg !574
  %245 = call i32 (...) @checkpoint(), !dbg !575
  br label %246, !dbg !576

; <label>:246:                                    ; preds = %131
  %247 = load i32, i32* %15, align 4, !dbg !577
  %248 = add i32 %247, 1, !dbg !577
  store i32 %248, i32* %15, align 4, !dbg !577
  %249 = load i32, i32* %17, align 4, !dbg !578
  %250 = add i32 %249, 1, !dbg !578
  store i32 %250, i32* %17, align 4, !dbg !578
  br label %127, !dbg !579, !llvm.loop !580

; <label>:251:                                    ; preds = %127
  %252 = call i32 (...) @checkpoint(), !dbg !582
  br label %253, !dbg !583

; <label>:253:                                    ; preds = %251
  %254 = load i32, i32* %18, align 4, !dbg !584
  %255 = load i32, i32* %14, align 4, !dbg !585
  %256 = add i32 %255, %254, !dbg !585
  store i32 %256, i32* %14, align 4, !dbg !585
  br label %113, !dbg !586, !llvm.loop !587

; <label>:257:                                    ; preds = %113
  %258 = load i32, i32* %18, align 4, !dbg !589
  store i32 %258, i32* %19, align 4, !dbg !590
  %259 = call i32 (...) @checkpoint(), !dbg !591
  br label %260, !dbg !592

; <label>:260:                                    ; preds = %257
  %261 = load i32, i32* %18, align 4, !dbg !593
  %262 = shl i32 %261, 1, !dbg !593
  store i32 %262, i32* %18, align 4, !dbg !593
  br label %90, !dbg !594, !llvm.loop !595

; <label>:263:                                    ; preds = %90
  %264 = load i32, i32* %8, align 4, !dbg !597
  %265 = icmp ne i32 %264, 0, !dbg !597
  br i1 %265, label %266, label %297, !dbg !599

; <label>:266:                                    ; preds = %263
  call void @llvm.dbg.declare(metadata double* %31, metadata !600, metadata !DIExpression()), !dbg !602
  %267 = load i32, i32* %7, align 4, !dbg !603
  %268 = uitofp i32 %267 to double, !dbg !604
  store double %268, double* %31, align 8, !dbg !602
  store i32 0, i32* %14, align 4, !dbg !605
  br label %269, !dbg !607

; <label>:269:                                    ; preds = %293, %266
  %270 = load i32, i32* %14, align 4, !dbg !608
  %271 = load i32, i32* %7, align 4, !dbg !610
  %272 = icmp ult i32 %270, %271, !dbg !611
  br i1 %272, label %273, label %296, !dbg !612

; <label>:273:                                    ; preds = %269
  %274 = load double, double* %31, align 8, !dbg !613
  %275 = load float*, float** %11, align 8, !dbg !615
  %276 = load i32, i32* %14, align 4, !dbg !616
  %277 = zext i32 %276 to i64, !dbg !615
  %278 = getelementptr inbounds float, float* %275, i64 %277, !dbg !615
  %279 = load float, float* %278, align 4, !dbg !617
  %280 = fpext float %279 to double, !dbg !617
  %281 = fdiv double %280, %274, !dbg !617
  %282 = fptrunc double %281 to float, !dbg !617
  store float %282, float* %278, align 4, !dbg !617
  %283 = load double, double* %31, align 8, !dbg !618
  %284 = load float*, float** %12, align 8, !dbg !619
  %285 = load i32, i32* %14, align 4, !dbg !620
  %286 = zext i32 %285 to i64, !dbg !619
  %287 = getelementptr inbounds float, float* %284, i64 %286, !dbg !619
  %288 = load float, float* %287, align 4, !dbg !621
  %289 = fpext float %288 to double, !dbg !621
  %290 = fdiv double %289, %283, !dbg !621
  %291 = fptrunc double %290 to float, !dbg !621
  store float %291, float* %287, align 4, !dbg !621
  %292 = call i32 (...) @checkpoint(), !dbg !622
  br label %293, !dbg !623

; <label>:293:                                    ; preds = %273
  %294 = load i32, i32* %14, align 4, !dbg !624
  %295 = add i32 %294, 1, !dbg !624
  store i32 %295, i32* %14, align 4, !dbg !624
  br label %269, !dbg !625, !llvm.loop !626

; <label>:296:                                    ; preds = %269
  br label %297, !dbg !628

; <label>:297:                                    ; preds = %296, %263
  ret void, !dbg !629
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @CheckPointer(i8*, i8*) #0 !dbg !630 {
  %3 = alloca i8*, align 8
  %4 = alloca i8*, align 8
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !635, metadata !DIExpression()), !dbg !636
  store i8* %1, i8** %4, align 8
  call void @llvm.dbg.declare(metadata i8** %4, metadata !637, metadata !DIExpression()), !dbg !638
  %5 = load i8*, i8** %3, align 8, !dbg !639
  %6 = icmp eq i8* %5, null, !dbg !641
  br i1 %6, label %7, label %8, !dbg !642

; <label>:7:                                      ; preds = %2
  call void @exit(i32 1) #6, !dbg !643
  unreachable, !dbg !643

; <label>:8:                                      ; preds = %2
  ret void, !dbg !645
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noreturn nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nounwind }
attributes #6 = { noreturn nounwind }

!llvm.dbg.cu = !{!2, !31, !35}
!llvm.ident = !{!39, !39, !39}
!llvm.module.flags = !{!40, !41, !42}

!0 = !DIGlobalVariableExpression(var: !1, expr: !DIExpression())
!1 = distinct !DIGlobalVariable(name: "invfft", scope: !2, file: !3, line: 7, type: !30, isLocal: false, isDefinition: true)
!2 = distinct !DICompileUnit(language: DW_LANG_C99, file: !3, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, globals: !5)
!3 = !DIFile(filename: "main.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/fft_stack")
!4 = !{}
!5 = !{!0, !6, !9, !11, !17, !19, !21, !23, !28}
!6 = !DIGlobalVariableExpression(var: !7, expr: !DIExpression())
!7 = distinct !DIGlobalVariable(name: "MAXWAVES", scope: !2, file: !3, line: 9, type: !8, isLocal: false, isDefinition: true)
!8 = !DIBasicType(name: "unsigned int", size: 32, encoding: DW_ATE_unsigned)
!9 = !DIGlobalVariableExpression(var: !10, expr: !DIExpression())
!10 = distinct !DIGlobalVariable(name: "MAXSIZE", scope: !2, file: !3, line: 8, type: !8, isLocal: false, isDefinition: true)
!11 = !DIGlobalVariableExpression(var: !12, expr: !DIExpression())
!12 = distinct !DIGlobalVariable(name: "realin", scope: !2, file: !3, line: 10, type: !13, isLocal: true, isDefinition: true)
!13 = !DICompositeType(tag: DW_TAG_array_type, baseType: !14, size: 32768, elements: !15)
!14 = !DIBasicType(name: "float", size: 32, encoding: DW_ATE_float)
!15 = !{!16}
!16 = !DISubrange(count: 1024)
!17 = !DIGlobalVariableExpression(var: !18, expr: !DIExpression())
!18 = distinct !DIGlobalVariable(name: "imagin", scope: !2, file: !3, line: 11, type: !13, isLocal: true, isDefinition: true)
!19 = !DIGlobalVariableExpression(var: !20, expr: !DIExpression())
!20 = distinct !DIGlobalVariable(name: "realout", scope: !2, file: !3, line: 12, type: !13, isLocal: true, isDefinition: true)
!21 = !DIGlobalVariableExpression(var: !22, expr: !DIExpression())
!22 = distinct !DIGlobalVariable(name: "imagout", scope: !2, file: !3, line: 13, type: !13, isLocal: true, isDefinition: true)
!23 = !DIGlobalVariableExpression(var: !24, expr: !DIExpression())
!24 = distinct !DIGlobalVariable(name: "Coeff", scope: !2, file: !3, line: 14, type: !25, isLocal: true, isDefinition: true)
!25 = !DICompositeType(tag: DW_TAG_array_type, baseType: !14, size: 512, elements: !26)
!26 = !{!27}
!27 = !DISubrange(count: 16)
!28 = !DIGlobalVariableExpression(var: !29, expr: !DIExpression())
!29 = distinct !DIGlobalVariable(name: "Amp", scope: !2, file: !3, line: 15, type: !25, isLocal: true, isDefinition: true)
!30 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!31 = distinct !DICompileUnit(language: DW_LANG_C99, file: !32, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, retainedTypes: !33)
!32 = !DIFile(filename: "fftmisc.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/fft_stack")
!33 = !{!34}
!34 = !DIBasicType(name: "double", size: 64, encoding: DW_ATE_float)
!35 = distinct !DICompileUnit(language: DW_LANG_C99, file: !36, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !4, retainedTypes: !37)
!36 = !DIFile(filename: "fourierf.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/fft_stack")
!37 = !{!38, !34}
!38 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: null, size: 64)
!39 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!40 = !{i32 2, !"Dwarf Version", i32 4}
!41 = !{i32 2, !"Debug Info Version", i32 3}
!42 = !{i32 1, !"wchar_size", i32 4}
!43 = distinct !DISubprogram(name: "main", scope: !3, file: !3, line: 20, type: !44, isLocal: false, isDefinition: true, scopeLine: 20, isOptimized: false, unit: !2, variables: !4)
!44 = !DISubroutineType(types: !45)
!45 = !{!30}
!46 = !DILocation(line: 21, column: 13, scope: !43)
!47 = !DILocation(line: 22, column: 5, scope: !43)
!48 = !DILocation(line: 23, column: 12, scope: !43)
!49 = !DILocation(line: 24, column: 13, scope: !43)
!50 = !DILocation(line: 25, column: 5, scope: !43)
!51 = !DILocation(line: 26, column: 5, scope: !43)
!52 = distinct !DISubprogram(name: "old_main", scope: !3, file: !3, line: 29, type: !44, isLocal: false, isDefinition: true, scopeLine: 29, isOptimized: false, unit: !2, variables: !4)
!53 = !DILocalVariable(name: "i", scope: !52, file: !3, line: 30, type: !8)
!54 = !DILocation(line: 30, column: 11, scope: !52)
!55 = !DILocalVariable(name: "j", scope: !52, file: !3, line: 30, type: !8)
!56 = !DILocation(line: 30, column: 13, scope: !52)
!57 = !DILocalVariable(name: "RealIn", scope: !52, file: !3, line: 31, type: !58)
!58 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !14, size: 64)
!59 = !DILocation(line: 31, column: 9, scope: !52)
!60 = !DILocalVariable(name: "ImagIn", scope: !52, file: !3, line: 32, type: !58)
!61 = !DILocation(line: 32, column: 9, scope: !52)
!62 = !DILocalVariable(name: "RealOut", scope: !52, file: !3, line: 33, type: !58)
!63 = !DILocation(line: 33, column: 9, scope: !52)
!64 = !DILocalVariable(name: "ImagOut", scope: !52, file: !3, line: 34, type: !58)
!65 = !DILocation(line: 34, column: 9, scope: !52)
!66 = !DILocalVariable(name: "coeff", scope: !52, file: !3, line: 35, type: !58)
!67 = !DILocation(line: 35, column: 9, scope: !52)
!68 = !DILocalVariable(name: "amp", scope: !52, file: !3, line: 36, type: !58)
!69 = !DILocation(line: 36, column: 9, scope: !52)
!70 = !DILocation(line: 39, column: 2, scope: !52)
!71 = !DILocation(line: 50, column: 9, scope: !52)
!72 = !DILocation(line: 51, column: 9, scope: !52)
!73 = !DILocation(line: 52, column: 10, scope: !52)
!74 = !DILocation(line: 53, column: 10, scope: !52)
!75 = !DILocation(line: 54, column: 8, scope: !52)
!76 = !DILocation(line: 55, column: 6, scope: !52)
!77 = !DILocation(line: 58, column: 7, scope: !78)
!78 = distinct !DILexicalBlock(scope: !52, file: !3, line: 58, column: 2)
!79 = !DILocation(line: 58, column: 6, scope: !78)
!80 = !DILocation(line: 58, column: 10, scope: !81)
!81 = distinct !DILexicalBlock(scope: !78, file: !3, line: 58, column: 2)
!82 = !DILocation(line: 58, column: 12, scope: !81)
!83 = !DILocation(line: 58, column: 11, scope: !81)
!84 = !DILocation(line: 58, column: 2, scope: !78)
!85 = !DILocation(line: 60, column: 14, scope: !86)
!86 = distinct !DILexicalBlock(scope: !81, file: !3, line: 59, column: 2)
!87 = !DILocation(line: 60, column: 20, scope: !86)
!88 = !DILocation(line: 60, column: 3, scope: !86)
!89 = !DILocation(line: 60, column: 9, scope: !86)
!90 = !DILocation(line: 60, column: 12, scope: !86)
!91 = !DILocation(line: 61, column: 12, scope: !86)
!92 = !DILocation(line: 61, column: 18, scope: !86)
!93 = !DILocation(line: 61, column: 3, scope: !86)
!94 = !DILocation(line: 61, column: 7, scope: !86)
!95 = !DILocation(line: 61, column: 10, scope: !86)
!96 = !DILocation(line: 62, column: 5, scope: !86)
!97 = !DILocation(line: 63, column: 2, scope: !86)
!98 = !DILocation(line: 58, column: 22, scope: !81)
!99 = !DILocation(line: 58, column: 2, scope: !81)
!100 = distinct !{!100, !84, !101}
!101 = !DILocation(line: 63, column: 2, scope: !78)
!102 = !DILocation(line: 64, column: 7, scope: !103)
!103 = distinct !DILexicalBlock(scope: !52, file: !3, line: 64, column: 2)
!104 = !DILocation(line: 64, column: 6, scope: !103)
!105 = !DILocation(line: 64, column: 10, scope: !106)
!106 = distinct !DILexicalBlock(scope: !103, file: !3, line: 64, column: 2)
!107 = !DILocation(line: 64, column: 12, scope: !106)
!108 = !DILocation(line: 64, column: 11, scope: !106)
!109 = !DILocation(line: 64, column: 2, scope: !103)
!110 = !DILocation(line: 67, column: 3, scope: !111)
!111 = distinct !DILexicalBlock(scope: !106, file: !3, line: 65, column: 2)
!112 = !DILocation(line: 67, column: 10, scope: !111)
!113 = !DILocation(line: 67, column: 12, scope: !111)
!114 = !DILocation(line: 68, column: 8, scope: !115)
!115 = distinct !DILexicalBlock(scope: !111, file: !3, line: 68, column: 3)
!116 = !DILocation(line: 68, column: 7, scope: !115)
!117 = !DILocation(line: 68, column: 11, scope: !118)
!118 = distinct !DILexicalBlock(scope: !115, file: !3, line: 68, column: 3)
!119 = !DILocation(line: 68, column: 13, scope: !118)
!120 = !DILocation(line: 68, column: 12, scope: !118)
!121 = !DILocation(line: 68, column: 3, scope: !115)
!122 = !DILocation(line: 71, column: 8, scope: !123)
!123 = distinct !DILexicalBlock(scope: !124, file: !3, line: 71, column: 8)
!124 = distinct !DILexicalBlock(scope: !118, file: !3, line: 69, column: 3)
!125 = !DILocation(line: 71, column: 14, scope: !123)
!126 = !DILocation(line: 71, column: 8, scope: !124)
!127 = !DILocation(line: 73, column: 17, scope: !128)
!128 = distinct !DILexicalBlock(scope: !123, file: !3, line: 72, column: 4)
!129 = !DILocation(line: 73, column: 23, scope: !128)
!130 = !DILocation(line: 73, column: 30, scope: !128)
!131 = !DILocation(line: 73, column: 34, scope: !128)
!132 = !DILocation(line: 73, column: 37, scope: !128)
!133 = !DILocation(line: 73, column: 36, scope: !128)
!134 = !DILocation(line: 73, column: 26, scope: !128)
!135 = !DILocation(line: 73, column: 25, scope: !128)
!136 = !DILocation(line: 73, column: 6, scope: !128)
!137 = !DILocation(line: 73, column: 13, scope: !128)
!138 = !DILocation(line: 73, column: 15, scope: !128)
!139 = !DILocation(line: 74, column: 4, scope: !128)
!140 = !DILocation(line: 77, column: 16, scope: !141)
!141 = distinct !DILexicalBlock(scope: !123, file: !3, line: 76, column: 4)
!142 = !DILocation(line: 77, column: 22, scope: !141)
!143 = !DILocation(line: 77, column: 29, scope: !141)
!144 = !DILocation(line: 77, column: 33, scope: !141)
!145 = !DILocation(line: 77, column: 36, scope: !141)
!146 = !DILocation(line: 77, column: 35, scope: !141)
!147 = !DILocation(line: 77, column: 25, scope: !141)
!148 = !DILocation(line: 77, column: 24, scope: !141)
!149 = !DILocation(line: 77, column: 5, scope: !141)
!150 = !DILocation(line: 77, column: 12, scope: !141)
!151 = !DILocation(line: 77, column: 14, scope: !141)
!152 = !DILocation(line: 79, column: 5, scope: !124)
!153 = !DILocation(line: 79, column: 12, scope: !124)
!154 = !DILocation(line: 79, column: 14, scope: !124)
!155 = !DILocation(line: 80, column: 6, scope: !124)
!156 = !DILocation(line: 81, column: 3, scope: !124)
!157 = !DILocation(line: 68, column: 23, scope: !118)
!158 = !DILocation(line: 68, column: 3, scope: !118)
!159 = distinct !{!159, !121, !160}
!160 = !DILocation(line: 81, column: 3, scope: !115)
!161 = !DILocation(line: 82, column: 4, scope: !111)
!162 = !DILocation(line: 83, column: 2, scope: !111)
!163 = !DILocation(line: 64, column: 21, scope: !106)
!164 = !DILocation(line: 64, column: 2, scope: !106)
!165 = distinct !{!165, !109, !166}
!166 = !DILocation(line: 83, column: 2, scope: !103)
!167 = !DILocation(line: 86, column: 13, scope: !52)
!168 = !DILocation(line: 86, column: 21, scope: !52)
!169 = !DILocation(line: 86, column: 28, scope: !52)
!170 = !DILocation(line: 86, column: 35, scope: !52)
!171 = !DILocation(line: 86, column: 42, scope: !52)
!172 = !DILocation(line: 86, column: 50, scope: !52)
!173 = !DILocation(line: 86, column: 2, scope: !52)
!174 = !DILocation(line: 88, column: 2, scope: !52)
!175 = !DILocation(line: 89, column: 8, scope: !176)
!176 = distinct !DILexicalBlock(scope: !52, file: !3, line: 89, column: 2)
!177 = !DILocation(line: 89, column: 7, scope: !176)
!178 = !DILocation(line: 89, column: 11, scope: !179)
!179 = distinct !DILexicalBlock(scope: !176, file: !3, line: 89, column: 2)
!180 = !DILocation(line: 89, column: 13, scope: !179)
!181 = !DILocation(line: 89, column: 12, scope: !179)
!182 = !DILocation(line: 89, column: 2, scope: !176)
!183 = !DILocation(line: 90, column: 20, scope: !184)
!184 = distinct !DILexicalBlock(scope: !179, file: !3, line: 89, column: 26)
!185 = !DILocation(line: 90, column: 28, scope: !184)
!186 = !DILocation(line: 90, column: 4, scope: !184)
!187 = !DILocation(line: 91, column: 4, scope: !184)
!188 = !DILocation(line: 92, column: 2, scope: !184)
!189 = !DILocation(line: 89, column: 22, scope: !179)
!190 = !DILocation(line: 89, column: 2, scope: !179)
!191 = distinct !{!191, !182, !192}
!192 = !DILocation(line: 92, column: 2, scope: !176)
!193 = !DILocation(line: 93, column: 2, scope: !52)
!194 = !DILocation(line: 95, column: 1, scope: !52)
!195 = !DILocation(line: 96, column: 8, scope: !196)
!196 = distinct !DILexicalBlock(scope: !52, file: !3, line: 96, column: 2)
!197 = !DILocation(line: 96, column: 7, scope: !196)
!198 = !DILocation(line: 96, column: 11, scope: !199)
!199 = distinct !DILexicalBlock(scope: !196, file: !3, line: 96, column: 2)
!200 = !DILocation(line: 96, column: 13, scope: !199)
!201 = !DILocation(line: 96, column: 12, scope: !199)
!202 = !DILocation(line: 96, column: 2, scope: !196)
!203 = !DILocation(line: 97, column: 20, scope: !204)
!204 = distinct !DILexicalBlock(scope: !199, file: !3, line: 96, column: 26)
!205 = !DILocation(line: 97, column: 28, scope: !204)
!206 = !DILocation(line: 97, column: 4, scope: !204)
!207 = !DILocation(line: 98, column: 4, scope: !204)
!208 = !DILocation(line: 99, column: 2, scope: !204)
!209 = !DILocation(line: 96, column: 22, scope: !199)
!210 = !DILocation(line: 96, column: 2, scope: !199)
!211 = distinct !{!211, !202, !212}
!212 = !DILocation(line: 99, column: 2, scope: !196)
!213 = !DILocation(line: 100, column: 2, scope: !52)
!214 = !DILocation(line: 108, column: 4, scope: !52)
!215 = distinct !DISubprogram(name: "IsPowerOfTwo", scope: !32, file: !32, line: 35, type: !216, isLocal: false, isDefinition: true, scopeLine: 36, flags: DIFlagPrototyped, isOptimized: false, unit: !31, variables: !4)
!216 = !DISubroutineType(types: !217)
!217 = !{!30, !8}
!218 = !DILocalVariable(name: "x", arg: 1, scope: !215, file: !32, line: 35, type: !8)
!219 = !DILocation(line: 35, column: 29, scope: !215)
!220 = !DILocation(line: 37, column: 10, scope: !221)
!221 = distinct !DILexicalBlock(scope: !215, file: !32, line: 37, column: 10)
!222 = !DILocation(line: 37, column: 12, scope: !221)
!223 = !DILocation(line: 37, column: 10, scope: !215)
!224 = !DILocation(line: 38, column: 9, scope: !221)
!225 = !DILocation(line: 40, column: 10, scope: !226)
!226 = distinct !DILexicalBlock(scope: !215, file: !32, line: 40, column: 10)
!227 = !DILocation(line: 40, column: 15, scope: !226)
!228 = !DILocation(line: 40, column: 16, scope: !226)
!229 = !DILocation(line: 40, column: 12, scope: !226)
!230 = !DILocation(line: 40, column: 10, scope: !215)
!231 = !DILocation(line: 41, column: 9, scope: !226)
!232 = !DILocation(line: 43, column: 5, scope: !215)
!233 = !DILocation(line: 44, column: 1, scope: !215)
!234 = distinct !DISubprogram(name: "NumberOfBitsNeeded", scope: !32, file: !32, line: 47, type: !235, isLocal: false, isDefinition: true, scopeLine: 48, flags: DIFlagPrototyped, isOptimized: false, unit: !31, variables: !4)
!235 = !DISubroutineType(types: !236)
!236 = !{!8, !8}
!237 = !DILocalVariable(name: "PowerOfTwo", arg: 1, scope: !234, file: !32, line: 47, type: !8)
!238 = !DILocation(line: 47, column: 40, scope: !234)
!239 = !DILocalVariable(name: "i", scope: !234, file: !32, line: 49, type: !8)
!240 = !DILocation(line: 49, column: 14, scope: !234)
!241 = !DILocation(line: 51, column: 10, scope: !242)
!242 = distinct !DILexicalBlock(scope: !234, file: !32, line: 51, column: 10)
!243 = !DILocation(line: 51, column: 21, scope: !242)
!244 = !DILocation(line: 51, column: 10, scope: !234)
!245 = !DILocation(line: 58, column: 9, scope: !246)
!246 = distinct !DILexicalBlock(scope: !242, file: !32, line: 52, column: 5)
!247 = !DILocation(line: 61, column: 12, scope: !248)
!248 = distinct !DILexicalBlock(scope: !234, file: !32, line: 61, column: 5)
!249 = !DILocation(line: 61, column: 11, scope: !248)
!250 = !DILocation(line: 63, column: 14, scope: !251)
!251 = distinct !DILexicalBlock(scope: !252, file: !32, line: 63, column: 14)
!252 = distinct !DILexicalBlock(scope: !253, file: !32, line: 62, column: 5)
!253 = distinct !DILexicalBlock(scope: !248, file: !32, line: 61, column: 5)
!254 = !DILocation(line: 63, column: 33, scope: !251)
!255 = !DILocation(line: 63, column: 30, scope: !251)
!256 = !DILocation(line: 63, column: 25, scope: !251)
!257 = !DILocation(line: 63, column: 14, scope: !252)
!258 = !DILocation(line: 64, column: 20, scope: !251)
!259 = !DILocation(line: 64, column: 13, scope: !251)
!260 = !DILocation(line: 66, column: 9, scope: !252)
!261 = !DILocation(line: 67, column: 5, scope: !252)
!262 = !DILocation(line: 61, column: 19, scope: !253)
!263 = !DILocation(line: 61, column: 5, scope: !253)
!264 = distinct !{!264, !265, !266}
!265 = !DILocation(line: 61, column: 5, scope: !248)
!266 = !DILocation(line: 67, column: 5, scope: !248)
!267 = distinct !DISubprogram(name: "ReverseBits", scope: !32, file: !32, line: 72, type: !268, isLocal: false, isDefinition: true, scopeLine: 73, flags: DIFlagPrototyped, isOptimized: false, unit: !31, variables: !4)
!268 = !DISubroutineType(types: !269)
!269 = !{!8, !8, !8}
!270 = !DILocalVariable(name: "index", arg: 1, scope: !267, file: !32, line: 72, type: !8)
!271 = !DILocation(line: 72, column: 33, scope: !267)
!272 = !DILocalVariable(name: "NumBits", arg: 2, scope: !267, file: !32, line: 72, type: !8)
!273 = !DILocation(line: 72, column: 49, scope: !267)
!274 = !DILocalVariable(name: "i", scope: !267, file: !32, line: 74, type: !8)
!275 = !DILocation(line: 74, column: 14, scope: !267)
!276 = !DILocalVariable(name: "rev", scope: !267, file: !32, line: 74, type: !8)
!277 = !DILocation(line: 74, column: 17, scope: !267)
!278 = !DILocation(line: 76, column: 16, scope: !279)
!279 = distinct !DILexicalBlock(scope: !267, file: !32, line: 76, column: 5)
!280 = !DILocation(line: 76, column: 12, scope: !279)
!281 = !DILocation(line: 76, column: 11, scope: !279)
!282 = !DILocation(line: 76, column: 20, scope: !283)
!283 = distinct !DILexicalBlock(scope: !279, file: !32, line: 76, column: 5)
!284 = !DILocation(line: 76, column: 24, scope: !283)
!285 = !DILocation(line: 76, column: 22, scope: !283)
!286 = !DILocation(line: 76, column: 5, scope: !279)
!287 = !DILocation(line: 78, column: 16, scope: !288)
!288 = distinct !DILexicalBlock(scope: !283, file: !32, line: 77, column: 5)
!289 = !DILocation(line: 78, column: 20, scope: !288)
!290 = !DILocation(line: 78, column: 29, scope: !288)
!291 = !DILocation(line: 78, column: 35, scope: !288)
!292 = !DILocation(line: 78, column: 26, scope: !288)
!293 = !DILocation(line: 78, column: 13, scope: !288)
!294 = !DILocation(line: 79, column: 15, scope: !288)
!295 = !DILocation(line: 81, column: 9, scope: !288)
!296 = !DILocation(line: 82, column: 5, scope: !288)
!297 = !DILocation(line: 76, column: 34, scope: !283)
!298 = !DILocation(line: 76, column: 5, scope: !283)
!299 = distinct !{!299, !286, !300}
!300 = !DILocation(line: 82, column: 5, scope: !279)
!301 = !DILocation(line: 84, column: 12, scope: !267)
!302 = !DILocation(line: 84, column: 5, scope: !267)
!303 = distinct !DISubprogram(name: "Index_to_frequency", scope: !32, file: !32, line: 88, type: !304, isLocal: false, isDefinition: true, scopeLine: 89, flags: DIFlagPrototyped, isOptimized: false, unit: !31, variables: !4)
!304 = !DISubroutineType(types: !305)
!305 = !{!34, !8, !8}
!306 = !DILocalVariable(name: "NumSamples", arg: 1, scope: !303, file: !32, line: 88, type: !8)
!307 = !DILocation(line: 88, column: 38, scope: !303)
!308 = !DILocalVariable(name: "Index", arg: 2, scope: !303, file: !32, line: 88, type: !8)
!309 = !DILocation(line: 88, column: 59, scope: !303)
!310 = !DILocation(line: 90, column: 10, scope: !311)
!311 = distinct !DILexicalBlock(scope: !303, file: !32, line: 90, column: 10)
!312 = !DILocation(line: 90, column: 19, scope: !311)
!313 = !DILocation(line: 90, column: 16, scope: !311)
!314 = !DILocation(line: 90, column: 10, scope: !303)
!315 = !DILocation(line: 91, column: 9, scope: !311)
!316 = !DILocation(line: 92, column: 15, scope: !317)
!317 = distinct !DILexicalBlock(scope: !311, file: !32, line: 92, column: 15)
!318 = !DILocation(line: 92, column: 24, scope: !317)
!319 = !DILocation(line: 92, column: 34, scope: !317)
!320 = !DILocation(line: 92, column: 21, scope: !317)
!321 = !DILocation(line: 92, column: 15, scope: !311)
!322 = !DILocation(line: 93, column: 24, scope: !317)
!323 = !DILocation(line: 93, column: 16, scope: !317)
!324 = !DILocation(line: 93, column: 40, scope: !317)
!325 = !DILocation(line: 93, column: 32, scope: !317)
!326 = !DILocation(line: 93, column: 30, scope: !317)
!327 = !DILocation(line: 93, column: 9, scope: !317)
!328 = !DILocation(line: 95, column: 22, scope: !303)
!329 = !DILocation(line: 95, column: 33, scope: !303)
!330 = !DILocation(line: 95, column: 32, scope: !303)
!331 = !DILocation(line: 95, column: 13, scope: !303)
!332 = !DILocation(line: 95, column: 12, scope: !303)
!333 = !DILocation(line: 95, column: 50, scope: !303)
!334 = !DILocation(line: 95, column: 42, scope: !303)
!335 = !DILocation(line: 95, column: 40, scope: !303)
!336 = !DILocation(line: 95, column: 5, scope: !303)
!337 = !DILocation(line: 96, column: 1, scope: !303)
!338 = distinct !DISubprogram(name: "fft_float", scope: !36, file: !36, line: 39, type: !339, isLocal: false, isDefinition: true, scopeLine: 46, flags: DIFlagPrototyped, isOptimized: false, unit: !35, variables: !4)
!339 = !DISubroutineType(types: !340)
!340 = !{null, !8, !30, !58, !58, !58, !58}
!341 = !DILocalVariable(name: "NumSamples", arg: 1, scope: !338, file: !36, line: 40, type: !8)
!342 = !DILocation(line: 40, column: 15, scope: !338)
!343 = !DILocalVariable(name: "InverseTransform", arg: 2, scope: !338, file: !36, line: 41, type: !30)
!344 = !DILocation(line: 41, column: 15, scope: !338)
!345 = !DILocalVariable(name: "RealIn", arg: 3, scope: !338, file: !36, line: 42, type: !58)
!346 = !DILocation(line: 42, column: 15, scope: !338)
!347 = !DILocalVariable(name: "ImagIn", arg: 4, scope: !338, file: !36, line: 43, type: !58)
!348 = !DILocation(line: 43, column: 15, scope: !338)
!349 = !DILocalVariable(name: "RealOut", arg: 5, scope: !338, file: !36, line: 44, type: !58)
!350 = !DILocation(line: 44, column: 15, scope: !338)
!351 = !DILocalVariable(name: "ImagOut", arg: 6, scope: !338, file: !36, line: 45, type: !58)
!352 = !DILocation(line: 45, column: 15, scope: !338)
!353 = !DILocalVariable(name: "NumBits", scope: !338, file: !36, line: 47, type: !8)
!354 = !DILocation(line: 47, column: 14, scope: !338)
!355 = !DILocalVariable(name: "i", scope: !338, file: !36, line: 48, type: !8)
!356 = !DILocation(line: 48, column: 14, scope: !338)
!357 = !DILocalVariable(name: "j", scope: !338, file: !36, line: 48, type: !8)
!358 = !DILocation(line: 48, column: 17, scope: !338)
!359 = !DILocalVariable(name: "k", scope: !338, file: !36, line: 48, type: !8)
!360 = !DILocation(line: 48, column: 20, scope: !338)
!361 = !DILocalVariable(name: "n", scope: !338, file: !36, line: 48, type: !8)
!362 = !DILocation(line: 48, column: 23, scope: !338)
!363 = !DILocalVariable(name: "BlockSize", scope: !338, file: !36, line: 49, type: !8)
!364 = !DILocation(line: 49, column: 14, scope: !338)
!365 = !DILocalVariable(name: "BlockEnd", scope: !338, file: !36, line: 49, type: !8)
!366 = !DILocation(line: 49, column: 25, scope: !338)
!367 = !DILocalVariable(name: "angle_numerator", scope: !338, file: !36, line: 51, type: !34)
!368 = !DILocation(line: 51, column: 12, scope: !338)
!369 = !DILocalVariable(name: "tr", scope: !338, file: !36, line: 52, type: !34)
!370 = !DILocation(line: 52, column: 12, scope: !338)
!371 = !DILocalVariable(name: "ti", scope: !338, file: !36, line: 52, type: !34)
!372 = !DILocation(line: 52, column: 16, scope: !338)
!373 = !DILocation(line: 54, column: 24, scope: !374)
!374 = distinct !DILexicalBlock(scope: !338, file: !36, line: 54, column: 10)
!375 = !DILocation(line: 54, column: 11, scope: !374)
!376 = !DILocation(line: 54, column: 10, scope: !338)
!377 = !DILocation(line: 61, column: 9, scope: !378)
!378 = distinct !DILexicalBlock(scope: !374, file: !36, line: 55, column: 5)
!379 = !DILocation(line: 64, column: 10, scope: !380)
!380 = distinct !DILexicalBlock(scope: !338, file: !36, line: 64, column: 10)
!381 = !DILocation(line: 64, column: 10, scope: !338)
!382 = !DILocation(line: 65, column: 28, scope: !380)
!383 = !DILocation(line: 65, column: 27, scope: !380)
!384 = !DILocation(line: 65, column: 25, scope: !380)
!385 = !DILocation(line: 65, column: 9, scope: !380)
!386 = !DILocation(line: 67, column: 5, scope: !338)
!387 = !DILocation(line: 68, column: 5, scope: !338)
!388 = !DILocation(line: 69, column: 5, scope: !338)
!389 = !DILocation(line: 71, column: 36, scope: !338)
!390 = !DILocation(line: 71, column: 15, scope: !338)
!391 = !DILocation(line: 71, column: 13, scope: !338)
!392 = !DILocation(line: 77, column: 12, scope: !393)
!393 = distinct !DILexicalBlock(scope: !338, file: !36, line: 77, column: 5)
!394 = !DILocation(line: 77, column: 11, scope: !393)
!395 = !DILocation(line: 77, column: 16, scope: !396)
!396 = distinct !DILexicalBlock(scope: !393, file: !36, line: 77, column: 5)
!397 = !DILocation(line: 77, column: 20, scope: !396)
!398 = !DILocation(line: 77, column: 18, scope: !396)
!399 = !DILocation(line: 77, column: 5, scope: !393)
!400 = !DILocation(line: 79, column: 27, scope: !401)
!401 = distinct !DILexicalBlock(scope: !396, file: !36, line: 78, column: 5)
!402 = !DILocation(line: 79, column: 30, scope: !401)
!403 = !DILocation(line: 79, column: 13, scope: !401)
!404 = !DILocation(line: 79, column: 11, scope: !401)
!405 = !DILocation(line: 80, column: 22, scope: !401)
!406 = !DILocation(line: 80, column: 29, scope: !401)
!407 = !DILocation(line: 80, column: 9, scope: !401)
!408 = !DILocation(line: 80, column: 17, scope: !401)
!409 = !DILocation(line: 80, column: 20, scope: !401)
!410 = !DILocation(line: 81, column: 23, scope: !401)
!411 = !DILocation(line: 81, column: 30, scope: !401)
!412 = !DILocation(line: 81, column: 22, scope: !401)
!413 = !DILocation(line: 81, column: 47, scope: !401)
!414 = !DILocation(line: 81, column: 54, scope: !401)
!415 = !DILocation(line: 81, column: 9, scope: !401)
!416 = !DILocation(line: 81, column: 17, scope: !401)
!417 = !DILocation(line: 81, column: 20, scope: !401)
!418 = !DILocation(line: 82, column: 9, scope: !401)
!419 = !DILocation(line: 83, column: 5, scope: !401)
!420 = !DILocation(line: 77, column: 33, scope: !396)
!421 = !DILocation(line: 77, column: 5, scope: !396)
!422 = distinct !{!422, !399, !423}
!423 = !DILocation(line: 83, column: 5, scope: !393)
!424 = !DILocation(line: 89, column: 14, scope: !338)
!425 = !DILocation(line: 90, column: 21, scope: !426)
!426 = distinct !DILexicalBlock(scope: !338, file: !36, line: 90, column: 5)
!427 = !DILocation(line: 90, column: 11, scope: !426)
!428 = !DILocation(line: 90, column: 26, scope: !429)
!429 = distinct !DILexicalBlock(scope: !426, file: !36, line: 90, column: 5)
!430 = !DILocation(line: 90, column: 39, scope: !429)
!431 = !DILocation(line: 90, column: 36, scope: !429)
!432 = !DILocation(line: 90, column: 5, scope: !426)
!433 = !DILocalVariable(name: "delta_angle", scope: !434, file: !36, line: 92, type: !34)
!434 = distinct !DILexicalBlock(scope: !429, file: !36, line: 91, column: 5)
!435 = !DILocation(line: 92, column: 16, scope: !434)
!436 = !DILocation(line: 92, column: 30, scope: !434)
!437 = !DILocation(line: 92, column: 56, scope: !434)
!438 = !DILocation(line: 92, column: 48, scope: !434)
!439 = !DILocation(line: 92, column: 46, scope: !434)
!440 = !DILocalVariable(name: "sm2", scope: !434, file: !36, line: 93, type: !34)
!441 = !DILocation(line: 93, column: 16, scope: !434)
!442 = !DILocation(line: 93, column: 33, scope: !434)
!443 = !DILocation(line: 93, column: 31, scope: !434)
!444 = !DILocation(line: 93, column: 22, scope: !434)
!445 = !DILocalVariable(name: "sm1", scope: !434, file: !36, line: 94, type: !34)
!446 = !DILocation(line: 94, column: 16, scope: !434)
!447 = !DILocation(line: 94, column: 29, scope: !434)
!448 = !DILocation(line: 94, column: 28, scope: !434)
!449 = !DILocation(line: 94, column: 22, scope: !434)
!450 = !DILocalVariable(name: "cm2", scope: !434, file: !36, line: 95, type: !34)
!451 = !DILocation(line: 95, column: 16, scope: !434)
!452 = !DILocation(line: 95, column: 33, scope: !434)
!453 = !DILocation(line: 95, column: 31, scope: !434)
!454 = !DILocation(line: 95, column: 22, scope: !434)
!455 = !DILocalVariable(name: "cm1", scope: !434, file: !36, line: 96, type: !34)
!456 = !DILocation(line: 96, column: 16, scope: !434)
!457 = !DILocation(line: 96, column: 29, scope: !434)
!458 = !DILocation(line: 96, column: 28, scope: !434)
!459 = !DILocation(line: 96, column: 22, scope: !434)
!460 = !DILocalVariable(name: "w", scope: !434, file: !36, line: 97, type: !34)
!461 = !DILocation(line: 97, column: 16, scope: !434)
!462 = !DILocation(line: 97, column: 24, scope: !434)
!463 = !DILocation(line: 97, column: 22, scope: !434)
!464 = !DILocalVariable(name: "ar", scope: !434, file: !36, line: 98, type: !465)
!465 = !DICompositeType(tag: DW_TAG_array_type, baseType: !34, size: 192, elements: !466)
!466 = !{!467}
!467 = !DISubrange(count: 3)
!468 = !DILocation(line: 98, column: 16, scope: !434)
!469 = !DILocalVariable(name: "ai", scope: !434, file: !36, line: 98, type: !465)
!470 = !DILocation(line: 98, column: 23, scope: !434)
!471 = !DILocation(line: 100, column: 16, scope: !472)
!472 = distinct !DILexicalBlock(scope: !434, file: !36, line: 100, column: 9)
!473 = !DILocation(line: 100, column: 15, scope: !472)
!474 = !DILocation(line: 100, column: 20, scope: !475)
!475 = distinct !DILexicalBlock(scope: !472, file: !36, line: 100, column: 9)
!476 = !DILocation(line: 100, column: 24, scope: !475)
!477 = !DILocation(line: 100, column: 22, scope: !475)
!478 = !DILocation(line: 100, column: 9, scope: !472)
!479 = !DILocation(line: 102, column: 21, scope: !480)
!480 = distinct !DILexicalBlock(scope: !475, file: !36, line: 101, column: 9)
!481 = !DILocation(line: 102, column: 13, scope: !480)
!482 = !DILocation(line: 102, column: 19, scope: !480)
!483 = !DILocation(line: 103, column: 21, scope: !480)
!484 = !DILocation(line: 103, column: 13, scope: !480)
!485 = !DILocation(line: 103, column: 19, scope: !480)
!486 = !DILocation(line: 105, column: 21, scope: !480)
!487 = !DILocation(line: 105, column: 13, scope: !480)
!488 = !DILocation(line: 105, column: 19, scope: !480)
!489 = !DILocation(line: 106, column: 21, scope: !480)
!490 = !DILocation(line: 106, column: 13, scope: !480)
!491 = !DILocation(line: 106, column: 19, scope: !480)
!492 = !DILocation(line: 108, column: 21, scope: !493)
!493 = distinct !DILexicalBlock(scope: !480, file: !36, line: 108, column: 13)
!494 = !DILocation(line: 108, column: 20, scope: !493)
!495 = !DILocation(line: 108, column: 25, scope: !493)
!496 = !DILocation(line: 108, column: 19, scope: !493)
!497 = !DILocation(line: 108, column: 29, scope: !498)
!498 = distinct !DILexicalBlock(scope: !493, file: !36, line: 108, column: 13)
!499 = !DILocation(line: 108, column: 33, scope: !498)
!500 = !DILocation(line: 108, column: 31, scope: !498)
!501 = !DILocation(line: 108, column: 13, scope: !493)
!502 = !DILocation(line: 110, column: 25, scope: !503)
!503 = distinct !DILexicalBlock(scope: !498, file: !36, line: 109, column: 13)
!504 = !DILocation(line: 110, column: 27, scope: !503)
!505 = !DILocation(line: 110, column: 26, scope: !503)
!506 = !DILocation(line: 110, column: 35, scope: !503)
!507 = !DILocation(line: 110, column: 33, scope: !503)
!508 = !DILocation(line: 110, column: 17, scope: !503)
!509 = !DILocation(line: 110, column: 23, scope: !503)
!510 = !DILocation(line: 111, column: 25, scope: !503)
!511 = !DILocation(line: 111, column: 17, scope: !503)
!512 = !DILocation(line: 111, column: 23, scope: !503)
!513 = !DILocation(line: 112, column: 25, scope: !503)
!514 = !DILocation(line: 112, column: 17, scope: !503)
!515 = !DILocation(line: 112, column: 23, scope: !503)
!516 = !DILocation(line: 114, column: 25, scope: !503)
!517 = !DILocation(line: 114, column: 27, scope: !503)
!518 = !DILocation(line: 114, column: 26, scope: !503)
!519 = !DILocation(line: 114, column: 35, scope: !503)
!520 = !DILocation(line: 114, column: 33, scope: !503)
!521 = !DILocation(line: 114, column: 17, scope: !503)
!522 = !DILocation(line: 114, column: 23, scope: !503)
!523 = !DILocation(line: 115, column: 25, scope: !503)
!524 = !DILocation(line: 115, column: 17, scope: !503)
!525 = !DILocation(line: 115, column: 23, scope: !503)
!526 = !DILocation(line: 116, column: 25, scope: !503)
!527 = !DILocation(line: 116, column: 17, scope: !503)
!528 = !DILocation(line: 116, column: 23, scope: !503)
!529 = !DILocation(line: 118, column: 21, scope: !503)
!530 = !DILocation(line: 118, column: 25, scope: !503)
!531 = !DILocation(line: 118, column: 23, scope: !503)
!532 = !DILocation(line: 118, column: 19, scope: !503)
!533 = !DILocation(line: 119, column: 22, scope: !503)
!534 = !DILocation(line: 119, column: 28, scope: !503)
!535 = !DILocation(line: 119, column: 36, scope: !503)
!536 = !DILocation(line: 119, column: 27, scope: !503)
!537 = !DILocation(line: 119, column: 41, scope: !503)
!538 = !DILocation(line: 119, column: 47, scope: !503)
!539 = !DILocation(line: 119, column: 55, scope: !503)
!540 = !DILocation(line: 119, column: 46, scope: !503)
!541 = !DILocation(line: 119, column: 39, scope: !503)
!542 = !DILocation(line: 119, column: 20, scope: !503)
!543 = !DILocation(line: 120, column: 22, scope: !503)
!544 = !DILocation(line: 120, column: 28, scope: !503)
!545 = !DILocation(line: 120, column: 36, scope: !503)
!546 = !DILocation(line: 120, column: 27, scope: !503)
!547 = !DILocation(line: 120, column: 41, scope: !503)
!548 = !DILocation(line: 120, column: 47, scope: !503)
!549 = !DILocation(line: 120, column: 55, scope: !503)
!550 = !DILocation(line: 120, column: 46, scope: !503)
!551 = !DILocation(line: 120, column: 39, scope: !503)
!552 = !DILocation(line: 120, column: 20, scope: !503)
!553 = !DILocation(line: 122, column: 30, scope: !503)
!554 = !DILocation(line: 122, column: 38, scope: !503)
!555 = !DILocation(line: 122, column: 43, scope: !503)
!556 = !DILocation(line: 122, column: 41, scope: !503)
!557 = !DILocation(line: 122, column: 17, scope: !503)
!558 = !DILocation(line: 122, column: 25, scope: !503)
!559 = !DILocation(line: 122, column: 28, scope: !503)
!560 = !DILocation(line: 123, column: 30, scope: !503)
!561 = !DILocation(line: 123, column: 38, scope: !503)
!562 = !DILocation(line: 123, column: 43, scope: !503)
!563 = !DILocation(line: 123, column: 41, scope: !503)
!564 = !DILocation(line: 123, column: 17, scope: !503)
!565 = !DILocation(line: 123, column: 25, scope: !503)
!566 = !DILocation(line: 123, column: 28, scope: !503)
!567 = !DILocation(line: 125, column: 31, scope: !503)
!568 = !DILocation(line: 125, column: 17, scope: !503)
!569 = !DILocation(line: 125, column: 25, scope: !503)
!570 = !DILocation(line: 125, column: 28, scope: !503)
!571 = !DILocation(line: 126, column: 31, scope: !503)
!572 = !DILocation(line: 126, column: 17, scope: !503)
!573 = !DILocation(line: 126, column: 25, scope: !503)
!574 = !DILocation(line: 126, column: 28, scope: !503)
!575 = !DILocation(line: 127, column: 17, scope: !503)
!576 = !DILocation(line: 128, column: 13, scope: !503)
!577 = !DILocation(line: 108, column: 44, scope: !498)
!578 = !DILocation(line: 108, column: 49, scope: !498)
!579 = !DILocation(line: 108, column: 13, scope: !498)
!580 = distinct !{!580, !501, !581}
!581 = !DILocation(line: 128, column: 13, scope: !493)
!582 = !DILocation(line: 129, column: 9, scope: !480)
!583 = !DILocation(line: 130, column: 9, scope: !480)
!584 = !DILocation(line: 100, column: 41, scope: !475)
!585 = !DILocation(line: 100, column: 38, scope: !475)
!586 = !DILocation(line: 100, column: 9, scope: !475)
!587 = distinct !{!587, !478, !588}
!588 = !DILocation(line: 130, column: 9, scope: !472)
!589 = !DILocation(line: 132, column: 20, scope: !434)
!590 = !DILocation(line: 132, column: 18, scope: !434)
!591 = !DILocation(line: 133, column: 9, scope: !434)
!592 = !DILocation(line: 134, column: 5, scope: !434)
!593 = !DILocation(line: 90, column: 61, scope: !429)
!594 = !DILocation(line: 90, column: 5, scope: !429)
!595 = distinct !{!595, !432, !596}
!596 = !DILocation(line: 134, column: 5, scope: !426)
!597 = !DILocation(line: 140, column: 10, scope: !598)
!598 = distinct !DILexicalBlock(scope: !338, file: !36, line: 140, column: 10)
!599 = !DILocation(line: 140, column: 10, scope: !338)
!600 = !DILocalVariable(name: "denom", scope: !601, file: !36, line: 142, type: !34)
!601 = distinct !DILexicalBlock(scope: !598, file: !36, line: 141, column: 5)
!602 = !DILocation(line: 142, column: 16, scope: !601)
!603 = !DILocation(line: 142, column: 32, scope: !601)
!604 = !DILocation(line: 142, column: 24, scope: !601)
!605 = !DILocation(line: 144, column: 16, scope: !606)
!606 = distinct !DILexicalBlock(scope: !601, file: !36, line: 144, column: 9)
!607 = !DILocation(line: 144, column: 15, scope: !606)
!608 = !DILocation(line: 144, column: 20, scope: !609)
!609 = distinct !DILexicalBlock(scope: !606, file: !36, line: 144, column: 9)
!610 = !DILocation(line: 144, column: 24, scope: !609)
!611 = !DILocation(line: 144, column: 22, scope: !609)
!612 = !DILocation(line: 144, column: 9, scope: !606)
!613 = !DILocation(line: 146, column: 27, scope: !614)
!614 = distinct !DILexicalBlock(scope: !609, file: !36, line: 145, column: 9)
!615 = !DILocation(line: 146, column: 13, scope: !614)
!616 = !DILocation(line: 146, column: 21, scope: !614)
!617 = !DILocation(line: 146, column: 24, scope: !614)
!618 = !DILocation(line: 147, column: 27, scope: !614)
!619 = !DILocation(line: 147, column: 13, scope: !614)
!620 = !DILocation(line: 147, column: 21, scope: !614)
!621 = !DILocation(line: 147, column: 24, scope: !614)
!622 = !DILocation(line: 148, column: 13, scope: !614)
!623 = !DILocation(line: 149, column: 9, scope: !614)
!624 = !DILocation(line: 144, column: 37, scope: !609)
!625 = !DILocation(line: 144, column: 9, scope: !609)
!626 = distinct !{!626, !612, !627}
!627 = !DILocation(line: 149, column: 9, scope: !606)
!628 = !DILocation(line: 150, column: 5, scope: !601)
!629 = !DILocation(line: 151, column: 1, scope: !338)
!630 = distinct !DISubprogram(name: "CheckPointer", scope: !36, file: !36, line: 29, type: !631, isLocal: true, isDefinition: true, scopeLine: 30, flags: DIFlagPrototyped, isOptimized: false, unit: !35, variables: !4)
!631 = !DISubroutineType(types: !632)
!632 = !{null, !38, !633}
!633 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !634, size: 64)
!634 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!635 = !DILocalVariable(name: "p", arg: 1, scope: !630, file: !36, line: 29, type: !38)
!636 = !DILocation(line: 29, column: 34, scope: !630)
!637 = !DILocalVariable(name: "name", arg: 2, scope: !630, file: !36, line: 29, type: !633)
!638 = !DILocation(line: 29, column: 43, scope: !630)
!639 = !DILocation(line: 31, column: 10, scope: !640)
!640 = distinct !DILexicalBlock(scope: !630, file: !36, line: 31, column: 10)
!641 = !DILocation(line: 31, column: 12, scope: !640)
!642 = !DILocation(line: 31, column: 10, scope: !630)
!643 = !DILocation(line: 34, column: 9, scope: !644)
!644 = distinct !DILexicalBlock(scope: !640, file: !36, line: 32, column: 5)
!645 = !DILocation(line: 36, column: 1, scope: !630)
