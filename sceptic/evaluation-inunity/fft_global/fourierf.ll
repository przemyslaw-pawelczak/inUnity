; ModuleID = 'fourierf.c'
source_filename = "fourierf.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"RealIn\00", align 1
@.str.1 = private unnamed_addr constant [8 x i8] c"RealOut\00", align 1
@.str.2 = private unnamed_addr constant [8 x i8] c"ImagOut\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define void @fft_float(i32, i32, float*, float*, float*, float*) #0 !dbg !10 {
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
  call void @llvm.dbg.declare(metadata i32* %7, metadata !17, metadata !DIExpression()), !dbg !18
  store i32 %1, i32* %8, align 4
  call void @llvm.dbg.declare(metadata i32* %8, metadata !19, metadata !DIExpression()), !dbg !20
  store float* %2, float** %9, align 8
  call void @llvm.dbg.declare(metadata float** %9, metadata !21, metadata !DIExpression()), !dbg !22
  store float* %3, float** %10, align 8
  call void @llvm.dbg.declare(metadata float** %10, metadata !23, metadata !DIExpression()), !dbg !24
  store float* %4, float** %11, align 8
  call void @llvm.dbg.declare(metadata float** %11, metadata !25, metadata !DIExpression()), !dbg !26
  store float* %5, float** %12, align 8
  call void @llvm.dbg.declare(metadata float** %12, metadata !27, metadata !DIExpression()), !dbg !28
  call void @llvm.dbg.declare(metadata i32* %13, metadata !29, metadata !DIExpression()), !dbg !30
  call void @llvm.dbg.declare(metadata i32* %14, metadata !31, metadata !DIExpression()), !dbg !32
  call void @llvm.dbg.declare(metadata i32* %15, metadata !33, metadata !DIExpression()), !dbg !34
  call void @llvm.dbg.declare(metadata i32* %16, metadata !35, metadata !DIExpression()), !dbg !36
  call void @llvm.dbg.declare(metadata i32* %17, metadata !37, metadata !DIExpression()), !dbg !38
  call void @llvm.dbg.declare(metadata i32* %18, metadata !39, metadata !DIExpression()), !dbg !40
  call void @llvm.dbg.declare(metadata i32* %19, metadata !41, metadata !DIExpression()), !dbg !42
  call void @llvm.dbg.declare(metadata double* %20, metadata !43, metadata !DIExpression()), !dbg !44
  store double 0x401921FB54442D18, double* %20, align 8, !dbg !44
  call void @llvm.dbg.declare(metadata double* %21, metadata !45, metadata !DIExpression()), !dbg !46
  call void @llvm.dbg.declare(metadata double* %22, metadata !47, metadata !DIExpression()), !dbg !48
  %32 = load i32, i32* %7, align 4, !dbg !49
  %33 = call i32 @IsPowerOfTwo(i32 %32), !dbg !51
  %34 = icmp ne i32 %33, 0, !dbg !51
  br i1 %34, label %36, label %35, !dbg !52

; <label>:35:                                     ; preds = %6
  call void @exit(i32 1) #5, !dbg !53
  unreachable, !dbg !53

; <label>:36:                                     ; preds = %6
  %37 = load i32, i32* %8, align 4, !dbg !55
  %38 = icmp ne i32 %37, 0, !dbg !55
  br i1 %38, label %39, label %42, !dbg !57

; <label>:39:                                     ; preds = %36
  %40 = load double, double* %20, align 8, !dbg !58
  %41 = fsub double -0.000000e+00, %40, !dbg !59
  store double %41, double* %20, align 8, !dbg !60
  br label %42, !dbg !61

; <label>:42:                                     ; preds = %39, %36
  %43 = load float*, float** %9, align 8, !dbg !62
  %44 = bitcast float* %43 to i8*, !dbg !62
  call void @CheckPointer(i8* %44, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str, i32 0, i32 0)), !dbg !62
  %45 = load float*, float** %11, align 8, !dbg !63
  %46 = bitcast float* %45 to i8*, !dbg !63
  call void @CheckPointer(i8* %46, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.1, i32 0, i32 0)), !dbg !63
  %47 = load float*, float** %12, align 8, !dbg !64
  %48 = bitcast float* %47 to i8*, !dbg !64
  call void @CheckPointer(i8* %48, i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.2, i32 0, i32 0)), !dbg !64
  %49 = load i32, i32* %7, align 4, !dbg !65
  %50 = call i32 @NumberOfBitsNeeded(i32 %49), !dbg !66
  store i32 %50, i32* %13, align 4, !dbg !67
  store i32 0, i32* %14, align 4, !dbg !68
  br label %51, !dbg !70

; <label>:51:                                     ; preds = %86, %42
  %52 = load i32, i32* %14, align 4, !dbg !71
  %53 = load i32, i32* %7, align 4, !dbg !73
  %54 = icmp ult i32 %52, %53, !dbg !74
  br i1 %54, label %55, label %89, !dbg !75

; <label>:55:                                     ; preds = %51
  %56 = load i32, i32* %14, align 4, !dbg !76
  %57 = load i32, i32* %13, align 4, !dbg !78
  %58 = call i32 @ReverseBits(i32 %56, i32 %57), !dbg !79
  store i32 %58, i32* %15, align 4, !dbg !80
  %59 = load float*, float** %9, align 8, !dbg !81
  %60 = load i32, i32* %14, align 4, !dbg !82
  %61 = zext i32 %60 to i64, !dbg !81
  %62 = getelementptr inbounds float, float* %59, i64 %61, !dbg !81
  %63 = load float, float* %62, align 4, !dbg !81
  %64 = load float*, float** %11, align 8, !dbg !83
  %65 = load i32, i32* %15, align 4, !dbg !84
  %66 = zext i32 %65 to i64, !dbg !83
  %67 = getelementptr inbounds float, float* %64, i64 %66, !dbg !83
  store float %63, float* %67, align 4, !dbg !85
  %68 = load float*, float** %10, align 8, !dbg !86
  %69 = icmp eq float* %68, null, !dbg !87
  br i1 %69, label %70, label %71, !dbg !88

; <label>:70:                                     ; preds = %55
  br label %78, !dbg !88

; <label>:71:                                     ; preds = %55
  %72 = load float*, float** %10, align 8, !dbg !89
  %73 = load i32, i32* %14, align 4, !dbg !90
  %74 = zext i32 %73 to i64, !dbg !89
  %75 = getelementptr inbounds float, float* %72, i64 %74, !dbg !89
  %76 = load float, float* %75, align 4, !dbg !89
  %77 = fpext float %76 to double, !dbg !89
  br label %78, !dbg !88

; <label>:78:                                     ; preds = %71, %70
  %79 = phi double [ 0.000000e+00, %70 ], [ %77, %71 ], !dbg !88
  %80 = fptrunc double %79 to float, !dbg !88
  %81 = load float*, float** %12, align 8, !dbg !91
  %82 = load i32, i32* %15, align 4, !dbg !92
  %83 = zext i32 %82 to i64, !dbg !91
  %84 = getelementptr inbounds float, float* %81, i64 %83, !dbg !91
  store float %80, float* %84, align 4, !dbg !93
  %85 = call i32 (...) @checkpoint(), !dbg !94
  br label %86, !dbg !95

; <label>:86:                                     ; preds = %78
  %87 = load i32, i32* %14, align 4, !dbg !96
  %88 = add i32 %87, 1, !dbg !96
  store i32 %88, i32* %14, align 4, !dbg !96
  br label %51, !dbg !97, !llvm.loop !98

; <label>:89:                                     ; preds = %51
  store i32 1, i32* %19, align 4, !dbg !100
  store i32 2, i32* %18, align 4, !dbg !101
  br label %90, !dbg !103

; <label>:90:                                     ; preds = %260, %89
  %91 = load i32, i32* %18, align 4, !dbg !104
  %92 = load i32, i32* %7, align 4, !dbg !106
  %93 = icmp ule i32 %91, %92, !dbg !107
  br i1 %93, label %94, label %263, !dbg !108

; <label>:94:                                     ; preds = %90
  call void @llvm.dbg.declare(metadata double* %23, metadata !109, metadata !DIExpression()), !dbg !111
  %95 = load double, double* %20, align 8, !dbg !112
  %96 = load i32, i32* %18, align 4, !dbg !113
  %97 = uitofp i32 %96 to double, !dbg !114
  %98 = fdiv double %95, %97, !dbg !115
  store double %98, double* %23, align 8, !dbg !111
  call void @llvm.dbg.declare(metadata double* %24, metadata !116, metadata !DIExpression()), !dbg !117
  %99 = load double, double* %23, align 8, !dbg !118
  %100 = fmul double -2.000000e+00, %99, !dbg !119
  %101 = call double @sin(double %100) #6, !dbg !120
  store double %101, double* %24, align 8, !dbg !117
  call void @llvm.dbg.declare(metadata double* %25, metadata !121, metadata !DIExpression()), !dbg !122
  %102 = load double, double* %23, align 8, !dbg !123
  %103 = fsub double -0.000000e+00, %102, !dbg !124
  %104 = call double @sin(double %103) #6, !dbg !125
  store double %104, double* %25, align 8, !dbg !122
  call void @llvm.dbg.declare(metadata double* %26, metadata !126, metadata !DIExpression()), !dbg !127
  %105 = load double, double* %23, align 8, !dbg !128
  %106 = fmul double -2.000000e+00, %105, !dbg !129
  %107 = call double @cos(double %106) #6, !dbg !130
  store double %107, double* %26, align 8, !dbg !127
  call void @llvm.dbg.declare(metadata double* %27, metadata !131, metadata !DIExpression()), !dbg !132
  %108 = load double, double* %23, align 8, !dbg !133
  %109 = fsub double -0.000000e+00, %108, !dbg !134
  %110 = call double @cos(double %109) #6, !dbg !135
  store double %110, double* %27, align 8, !dbg !132
  call void @llvm.dbg.declare(metadata double* %28, metadata !136, metadata !DIExpression()), !dbg !137
  %111 = load double, double* %27, align 8, !dbg !138
  %112 = fmul double 2.000000e+00, %111, !dbg !139
  store double %112, double* %28, align 8, !dbg !137
  call void @llvm.dbg.declare(metadata [3 x double]* %29, metadata !140, metadata !DIExpression()), !dbg !144
  call void @llvm.dbg.declare(metadata [3 x double]* %30, metadata !145, metadata !DIExpression()), !dbg !146
  store i32 0, i32* %14, align 4, !dbg !147
  br label %113, !dbg !149

; <label>:113:                                    ; preds = %253, %94
  %114 = load i32, i32* %14, align 4, !dbg !150
  %115 = load i32, i32* %7, align 4, !dbg !152
  %116 = icmp ult i32 %114, %115, !dbg !153
  br i1 %116, label %117, label %257, !dbg !154

; <label>:117:                                    ; preds = %113
  %118 = load double, double* %26, align 8, !dbg !155
  %119 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 2, !dbg !157
  store double %118, double* %119, align 16, !dbg !158
  %120 = load double, double* %27, align 8, !dbg !159
  %121 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !160
  store double %120, double* %121, align 8, !dbg !161
  %122 = load double, double* %24, align 8, !dbg !162
  %123 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 2, !dbg !163
  store double %122, double* %123, align 16, !dbg !164
  %124 = load double, double* %25, align 8, !dbg !165
  %125 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !166
  store double %124, double* %125, align 8, !dbg !167
  %126 = load i32, i32* %14, align 4, !dbg !168
  store i32 %126, i32* %15, align 4, !dbg !170
  store i32 0, i32* %17, align 4, !dbg !171
  br label %127, !dbg !172

; <label>:127:                                    ; preds = %246, %117
  %128 = load i32, i32* %17, align 4, !dbg !173
  %129 = load i32, i32* %19, align 4, !dbg !175
  %130 = icmp ult i32 %128, %129, !dbg !176
  br i1 %130, label %131, label %251, !dbg !177

; <label>:131:                                    ; preds = %127
  %132 = load double, double* %28, align 8, !dbg !178
  %133 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !180
  %134 = load double, double* %133, align 8, !dbg !180
  %135 = fmul double %132, %134, !dbg !181
  %136 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 2, !dbg !182
  %137 = load double, double* %136, align 16, !dbg !182
  %138 = fsub double %135, %137, !dbg !183
  %139 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !184
  store double %138, double* %139, align 16, !dbg !185
  %140 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !186
  %141 = load double, double* %140, align 8, !dbg !186
  %142 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 2, !dbg !187
  store double %141, double* %142, align 16, !dbg !188
  %143 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !189
  %144 = load double, double* %143, align 16, !dbg !189
  %145 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 1, !dbg !190
  store double %144, double* %145, align 8, !dbg !191
  %146 = load double, double* %28, align 8, !dbg !192
  %147 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !193
  %148 = load double, double* %147, align 8, !dbg !193
  %149 = fmul double %146, %148, !dbg !194
  %150 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 2, !dbg !195
  %151 = load double, double* %150, align 16, !dbg !195
  %152 = fsub double %149, %151, !dbg !196
  %153 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !197
  store double %152, double* %153, align 16, !dbg !198
  %154 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !199
  %155 = load double, double* %154, align 8, !dbg !199
  %156 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 2, !dbg !200
  store double %155, double* %156, align 16, !dbg !201
  %157 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !202
  %158 = load double, double* %157, align 16, !dbg !202
  %159 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 1, !dbg !203
  store double %158, double* %159, align 8, !dbg !204
  %160 = load i32, i32* %15, align 4, !dbg !205
  %161 = load i32, i32* %19, align 4, !dbg !206
  %162 = add i32 %160, %161, !dbg !207
  store i32 %162, i32* %16, align 4, !dbg !208
  %163 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !209
  %164 = load double, double* %163, align 16, !dbg !209
  %165 = load float*, float** %11, align 8, !dbg !210
  %166 = load i32, i32* %16, align 4, !dbg !211
  %167 = zext i32 %166 to i64, !dbg !210
  %168 = getelementptr inbounds float, float* %165, i64 %167, !dbg !210
  %169 = load float, float* %168, align 4, !dbg !210
  %170 = fpext float %169 to double, !dbg !210
  %171 = fmul double %164, %170, !dbg !212
  %172 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !213
  %173 = load double, double* %172, align 16, !dbg !213
  %174 = load float*, float** %12, align 8, !dbg !214
  %175 = load i32, i32* %16, align 4, !dbg !215
  %176 = zext i32 %175 to i64, !dbg !214
  %177 = getelementptr inbounds float, float* %174, i64 %176, !dbg !214
  %178 = load float, float* %177, align 4, !dbg !214
  %179 = fpext float %178 to double, !dbg !214
  %180 = fmul double %173, %179, !dbg !216
  %181 = fsub double %171, %180, !dbg !217
  store double %181, double* %21, align 8, !dbg !218
  %182 = getelementptr inbounds [3 x double], [3 x double]* %29, i64 0, i64 0, !dbg !219
  %183 = load double, double* %182, align 16, !dbg !219
  %184 = load float*, float** %12, align 8, !dbg !220
  %185 = load i32, i32* %16, align 4, !dbg !221
  %186 = zext i32 %185 to i64, !dbg !220
  %187 = getelementptr inbounds float, float* %184, i64 %186, !dbg !220
  %188 = load float, float* %187, align 4, !dbg !220
  %189 = fpext float %188 to double, !dbg !220
  %190 = fmul double %183, %189, !dbg !222
  %191 = getelementptr inbounds [3 x double], [3 x double]* %30, i64 0, i64 0, !dbg !223
  %192 = load double, double* %191, align 16, !dbg !223
  %193 = load float*, float** %11, align 8, !dbg !224
  %194 = load i32, i32* %16, align 4, !dbg !225
  %195 = zext i32 %194 to i64, !dbg !224
  %196 = getelementptr inbounds float, float* %193, i64 %195, !dbg !224
  %197 = load float, float* %196, align 4, !dbg !224
  %198 = fpext float %197 to double, !dbg !224
  %199 = fmul double %192, %198, !dbg !226
  %200 = fadd double %190, %199, !dbg !227
  store double %200, double* %22, align 8, !dbg !228
  %201 = load float*, float** %11, align 8, !dbg !229
  %202 = load i32, i32* %15, align 4, !dbg !230
  %203 = zext i32 %202 to i64, !dbg !229
  %204 = getelementptr inbounds float, float* %201, i64 %203, !dbg !229
  %205 = load float, float* %204, align 4, !dbg !229
  %206 = fpext float %205 to double, !dbg !229
  %207 = load double, double* %21, align 8, !dbg !231
  %208 = fsub double %206, %207, !dbg !232
  %209 = fptrunc double %208 to float, !dbg !229
  %210 = load float*, float** %11, align 8, !dbg !233
  %211 = load i32, i32* %16, align 4, !dbg !234
  %212 = zext i32 %211 to i64, !dbg !233
  %213 = getelementptr inbounds float, float* %210, i64 %212, !dbg !233
  store float %209, float* %213, align 4, !dbg !235
  %214 = load float*, float** %12, align 8, !dbg !236
  %215 = load i32, i32* %15, align 4, !dbg !237
  %216 = zext i32 %215 to i64, !dbg !236
  %217 = getelementptr inbounds float, float* %214, i64 %216, !dbg !236
  %218 = load float, float* %217, align 4, !dbg !236
  %219 = fpext float %218 to double, !dbg !236
  %220 = load double, double* %22, align 8, !dbg !238
  %221 = fsub double %219, %220, !dbg !239
  %222 = fptrunc double %221 to float, !dbg !236
  %223 = load float*, float** %12, align 8, !dbg !240
  %224 = load i32, i32* %16, align 4, !dbg !241
  %225 = zext i32 %224 to i64, !dbg !240
  %226 = getelementptr inbounds float, float* %223, i64 %225, !dbg !240
  store float %222, float* %226, align 4, !dbg !242
  %227 = load double, double* %21, align 8, !dbg !243
  %228 = load float*, float** %11, align 8, !dbg !244
  %229 = load i32, i32* %15, align 4, !dbg !245
  %230 = zext i32 %229 to i64, !dbg !244
  %231 = getelementptr inbounds float, float* %228, i64 %230, !dbg !244
  %232 = load float, float* %231, align 4, !dbg !246
  %233 = fpext float %232 to double, !dbg !246
  %234 = fadd double %233, %227, !dbg !246
  %235 = fptrunc double %234 to float, !dbg !246
  store float %235, float* %231, align 4, !dbg !246
  %236 = load double, double* %22, align 8, !dbg !247
  %237 = load float*, float** %12, align 8, !dbg !248
  %238 = load i32, i32* %15, align 4, !dbg !249
  %239 = zext i32 %238 to i64, !dbg !248
  %240 = getelementptr inbounds float, float* %237, i64 %239, !dbg !248
  %241 = load float, float* %240, align 4, !dbg !250
  %242 = fpext float %241 to double, !dbg !250
  %243 = fadd double %242, %236, !dbg !250
  %244 = fptrunc double %243 to float, !dbg !250
  store float %244, float* %240, align 4, !dbg !250
  %245 = call i32 (...) @checkpoint(), !dbg !251
  br label %246, !dbg !252

; <label>:246:                                    ; preds = %131
  %247 = load i32, i32* %15, align 4, !dbg !253
  %248 = add i32 %247, 1, !dbg !253
  store i32 %248, i32* %15, align 4, !dbg !253
  %249 = load i32, i32* %17, align 4, !dbg !254
  %250 = add i32 %249, 1, !dbg !254
  store i32 %250, i32* %17, align 4, !dbg !254
  br label %127, !dbg !255, !llvm.loop !256

; <label>:251:                                    ; preds = %127
  %252 = call i32 (...) @checkpoint(), !dbg !258
  br label %253, !dbg !259

; <label>:253:                                    ; preds = %251
  %254 = load i32, i32* %18, align 4, !dbg !260
  %255 = load i32, i32* %14, align 4, !dbg !261
  %256 = add i32 %255, %254, !dbg !261
  store i32 %256, i32* %14, align 4, !dbg !261
  br label %113, !dbg !262, !llvm.loop !263

; <label>:257:                                    ; preds = %113
  %258 = load i32, i32* %18, align 4, !dbg !265
  store i32 %258, i32* %19, align 4, !dbg !266
  %259 = call i32 (...) @checkpoint(), !dbg !267
  br label %260, !dbg !268

; <label>:260:                                    ; preds = %257
  %261 = load i32, i32* %18, align 4, !dbg !269
  %262 = shl i32 %261, 1, !dbg !269
  store i32 %262, i32* %18, align 4, !dbg !269
  br label %90, !dbg !270, !llvm.loop !271

; <label>:263:                                    ; preds = %90
  %264 = load i32, i32* %8, align 4, !dbg !273
  %265 = icmp ne i32 %264, 0, !dbg !273
  br i1 %265, label %266, label %297, !dbg !275

; <label>:266:                                    ; preds = %263
  call void @llvm.dbg.declare(metadata double* %31, metadata !276, metadata !DIExpression()), !dbg !278
  %267 = load i32, i32* %7, align 4, !dbg !279
  %268 = uitofp i32 %267 to double, !dbg !280
  store double %268, double* %31, align 8, !dbg !278
  store i32 0, i32* %14, align 4, !dbg !281
  br label %269, !dbg !283

; <label>:269:                                    ; preds = %293, %266
  %270 = load i32, i32* %14, align 4, !dbg !284
  %271 = load i32, i32* %7, align 4, !dbg !286
  %272 = icmp ult i32 %270, %271, !dbg !287
  br i1 %272, label %273, label %296, !dbg !288

; <label>:273:                                    ; preds = %269
  %274 = load double, double* %31, align 8, !dbg !289
  %275 = load float*, float** %11, align 8, !dbg !291
  %276 = load i32, i32* %14, align 4, !dbg !292
  %277 = zext i32 %276 to i64, !dbg !291
  %278 = getelementptr inbounds float, float* %275, i64 %277, !dbg !291
  %279 = load float, float* %278, align 4, !dbg !293
  %280 = fpext float %279 to double, !dbg !293
  %281 = fdiv double %280, %274, !dbg !293
  %282 = fptrunc double %281 to float, !dbg !293
  store float %282, float* %278, align 4, !dbg !293
  %283 = load double, double* %31, align 8, !dbg !294
  %284 = load float*, float** %12, align 8, !dbg !295
  %285 = load i32, i32* %14, align 4, !dbg !296
  %286 = zext i32 %285 to i64, !dbg !295
  %287 = getelementptr inbounds float, float* %284, i64 %286, !dbg !295
  %288 = load float, float* %287, align 4, !dbg !297
  %289 = fpext float %288 to double, !dbg !297
  %290 = fdiv double %289, %283, !dbg !297
  %291 = fptrunc double %290 to float, !dbg !297
  store float %291, float* %287, align 4, !dbg !297
  %292 = call i32 (...) @checkpoint(), !dbg !298
  br label %293, !dbg !299

; <label>:293:                                    ; preds = %273
  %294 = load i32, i32* %14, align 4, !dbg !300
  %295 = add i32 %294, 1, !dbg !300
  store i32 %295, i32* %14, align 4, !dbg !300
  br label %269, !dbg !301, !llvm.loop !302

; <label>:296:                                    ; preds = %269
  br label %297, !dbg !304

; <label>:297:                                    ; preds = %296, %263
  ret void, !dbg !305
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

declare i32 @IsPowerOfTwo(i32) #2

; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

; Function Attrs: noinline nounwind optnone uwtable
define internal void @CheckPointer(i8*, i8*) #0 !dbg !306 {
  %3 = alloca i8*, align 8
  %4 = alloca i8*, align 8
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !311, metadata !DIExpression()), !dbg !312
  store i8* %1, i8** %4, align 8
  call void @llvm.dbg.declare(metadata i8** %4, metadata !313, metadata !DIExpression()), !dbg !314
  %5 = load i8*, i8** %3, align 8, !dbg !315
  %6 = icmp eq i8* %5, null, !dbg !317
  br i1 %6, label %7, label %8, !dbg !318

; <label>:7:                                      ; preds = %2
  call void @exit(i32 1) #5, !dbg !319
  unreachable, !dbg !319

; <label>:8:                                      ; preds = %2
  ret void, !dbg !321
}

declare i32 @NumberOfBitsNeeded(i32) #2

declare i32 @ReverseBits(i32, i32) #2

declare i32 @checkpoint(...) #2

; Function Attrs: nounwind
declare double @sin(double) #4

; Function Attrs: nounwind
declare double @cos(double) #4

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noreturn nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { noreturn nounwind }
attributes #6 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!6, !7, !8}
!llvm.ident = !{!9}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 6.0.1 (tags/RELEASE_601/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, retainedTypes: !3)
!1 = !DIFile(filename: "fourierf.c", directory: "/home/felix/Desktop/inUnity/sceptic/evaluation-inunity/fft_global")
!2 = !{}
!3 = !{!4, !5}
!4 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: null, size: 64)
!5 = !DIBasicType(name: "double", size: 64, encoding: DW_ATE_float)
!6 = !{i32 2, !"Dwarf Version", i32 4}
!7 = !{i32 2, !"Debug Info Version", i32 3}
!8 = !{i32 1, !"wchar_size", i32 4}
!9 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
!10 = distinct !DISubprogram(name: "fft_float", scope: !1, file: !1, line: 39, type: !11, isLocal: false, isDefinition: true, scopeLine: 46, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!11 = !DISubroutineType(types: !12)
!12 = !{null, !13, !14, !15, !15, !15, !15}
!13 = !DIBasicType(name: "unsigned int", size: 32, encoding: DW_ATE_unsigned)
!14 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!15 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !16, size: 64)
!16 = !DIBasicType(name: "float", size: 32, encoding: DW_ATE_float)
!17 = !DILocalVariable(name: "NumSamples", arg: 1, scope: !10, file: !1, line: 40, type: !13)
!18 = !DILocation(line: 40, column: 15, scope: !10)
!19 = !DILocalVariable(name: "InverseTransform", arg: 2, scope: !10, file: !1, line: 41, type: !14)
!20 = !DILocation(line: 41, column: 15, scope: !10)
!21 = !DILocalVariable(name: "RealIn", arg: 3, scope: !10, file: !1, line: 42, type: !15)
!22 = !DILocation(line: 42, column: 15, scope: !10)
!23 = !DILocalVariable(name: "ImagIn", arg: 4, scope: !10, file: !1, line: 43, type: !15)
!24 = !DILocation(line: 43, column: 15, scope: !10)
!25 = !DILocalVariable(name: "RealOut", arg: 5, scope: !10, file: !1, line: 44, type: !15)
!26 = !DILocation(line: 44, column: 15, scope: !10)
!27 = !DILocalVariable(name: "ImagOut", arg: 6, scope: !10, file: !1, line: 45, type: !15)
!28 = !DILocation(line: 45, column: 15, scope: !10)
!29 = !DILocalVariable(name: "NumBits", scope: !10, file: !1, line: 47, type: !13)
!30 = !DILocation(line: 47, column: 14, scope: !10)
!31 = !DILocalVariable(name: "i", scope: !10, file: !1, line: 48, type: !13)
!32 = !DILocation(line: 48, column: 14, scope: !10)
!33 = !DILocalVariable(name: "j", scope: !10, file: !1, line: 48, type: !13)
!34 = !DILocation(line: 48, column: 17, scope: !10)
!35 = !DILocalVariable(name: "k", scope: !10, file: !1, line: 48, type: !13)
!36 = !DILocation(line: 48, column: 20, scope: !10)
!37 = !DILocalVariable(name: "n", scope: !10, file: !1, line: 48, type: !13)
!38 = !DILocation(line: 48, column: 23, scope: !10)
!39 = !DILocalVariable(name: "BlockSize", scope: !10, file: !1, line: 49, type: !13)
!40 = !DILocation(line: 49, column: 14, scope: !10)
!41 = !DILocalVariable(name: "BlockEnd", scope: !10, file: !1, line: 49, type: !13)
!42 = !DILocation(line: 49, column: 25, scope: !10)
!43 = !DILocalVariable(name: "angle_numerator", scope: !10, file: !1, line: 51, type: !5)
!44 = !DILocation(line: 51, column: 12, scope: !10)
!45 = !DILocalVariable(name: "tr", scope: !10, file: !1, line: 52, type: !5)
!46 = !DILocation(line: 52, column: 12, scope: !10)
!47 = !DILocalVariable(name: "ti", scope: !10, file: !1, line: 52, type: !5)
!48 = !DILocation(line: 52, column: 16, scope: !10)
!49 = !DILocation(line: 54, column: 24, scope: !50)
!50 = distinct !DILexicalBlock(scope: !10, file: !1, line: 54, column: 10)
!51 = !DILocation(line: 54, column: 11, scope: !50)
!52 = !DILocation(line: 54, column: 10, scope: !10)
!53 = !DILocation(line: 61, column: 9, scope: !54)
!54 = distinct !DILexicalBlock(scope: !50, file: !1, line: 55, column: 5)
!55 = !DILocation(line: 64, column: 10, scope: !56)
!56 = distinct !DILexicalBlock(scope: !10, file: !1, line: 64, column: 10)
!57 = !DILocation(line: 64, column: 10, scope: !10)
!58 = !DILocation(line: 65, column: 28, scope: !56)
!59 = !DILocation(line: 65, column: 27, scope: !56)
!60 = !DILocation(line: 65, column: 25, scope: !56)
!61 = !DILocation(line: 65, column: 9, scope: !56)
!62 = !DILocation(line: 67, column: 5, scope: !10)
!63 = !DILocation(line: 68, column: 5, scope: !10)
!64 = !DILocation(line: 69, column: 5, scope: !10)
!65 = !DILocation(line: 71, column: 36, scope: !10)
!66 = !DILocation(line: 71, column: 15, scope: !10)
!67 = !DILocation(line: 71, column: 13, scope: !10)
!68 = !DILocation(line: 77, column: 12, scope: !69)
!69 = distinct !DILexicalBlock(scope: !10, file: !1, line: 77, column: 5)
!70 = !DILocation(line: 77, column: 11, scope: !69)
!71 = !DILocation(line: 77, column: 16, scope: !72)
!72 = distinct !DILexicalBlock(scope: !69, file: !1, line: 77, column: 5)
!73 = !DILocation(line: 77, column: 20, scope: !72)
!74 = !DILocation(line: 77, column: 18, scope: !72)
!75 = !DILocation(line: 77, column: 5, scope: !69)
!76 = !DILocation(line: 79, column: 27, scope: !77)
!77 = distinct !DILexicalBlock(scope: !72, file: !1, line: 78, column: 5)
!78 = !DILocation(line: 79, column: 30, scope: !77)
!79 = !DILocation(line: 79, column: 13, scope: !77)
!80 = !DILocation(line: 79, column: 11, scope: !77)
!81 = !DILocation(line: 80, column: 22, scope: !77)
!82 = !DILocation(line: 80, column: 29, scope: !77)
!83 = !DILocation(line: 80, column: 9, scope: !77)
!84 = !DILocation(line: 80, column: 17, scope: !77)
!85 = !DILocation(line: 80, column: 20, scope: !77)
!86 = !DILocation(line: 81, column: 23, scope: !77)
!87 = !DILocation(line: 81, column: 30, scope: !77)
!88 = !DILocation(line: 81, column: 22, scope: !77)
!89 = !DILocation(line: 81, column: 47, scope: !77)
!90 = !DILocation(line: 81, column: 54, scope: !77)
!91 = !DILocation(line: 81, column: 9, scope: !77)
!92 = !DILocation(line: 81, column: 17, scope: !77)
!93 = !DILocation(line: 81, column: 20, scope: !77)
!94 = !DILocation(line: 82, column: 9, scope: !77)
!95 = !DILocation(line: 83, column: 5, scope: !77)
!96 = !DILocation(line: 77, column: 33, scope: !72)
!97 = !DILocation(line: 77, column: 5, scope: !72)
!98 = distinct !{!98, !75, !99}
!99 = !DILocation(line: 83, column: 5, scope: !69)
!100 = !DILocation(line: 89, column: 14, scope: !10)
!101 = !DILocation(line: 90, column: 21, scope: !102)
!102 = distinct !DILexicalBlock(scope: !10, file: !1, line: 90, column: 5)
!103 = !DILocation(line: 90, column: 11, scope: !102)
!104 = !DILocation(line: 90, column: 26, scope: !105)
!105 = distinct !DILexicalBlock(scope: !102, file: !1, line: 90, column: 5)
!106 = !DILocation(line: 90, column: 39, scope: !105)
!107 = !DILocation(line: 90, column: 36, scope: !105)
!108 = !DILocation(line: 90, column: 5, scope: !102)
!109 = !DILocalVariable(name: "delta_angle", scope: !110, file: !1, line: 92, type: !5)
!110 = distinct !DILexicalBlock(scope: !105, file: !1, line: 91, column: 5)
!111 = !DILocation(line: 92, column: 16, scope: !110)
!112 = !DILocation(line: 92, column: 30, scope: !110)
!113 = !DILocation(line: 92, column: 56, scope: !110)
!114 = !DILocation(line: 92, column: 48, scope: !110)
!115 = !DILocation(line: 92, column: 46, scope: !110)
!116 = !DILocalVariable(name: "sm2", scope: !110, file: !1, line: 93, type: !5)
!117 = !DILocation(line: 93, column: 16, scope: !110)
!118 = !DILocation(line: 93, column: 33, scope: !110)
!119 = !DILocation(line: 93, column: 31, scope: !110)
!120 = !DILocation(line: 93, column: 22, scope: !110)
!121 = !DILocalVariable(name: "sm1", scope: !110, file: !1, line: 94, type: !5)
!122 = !DILocation(line: 94, column: 16, scope: !110)
!123 = !DILocation(line: 94, column: 29, scope: !110)
!124 = !DILocation(line: 94, column: 28, scope: !110)
!125 = !DILocation(line: 94, column: 22, scope: !110)
!126 = !DILocalVariable(name: "cm2", scope: !110, file: !1, line: 95, type: !5)
!127 = !DILocation(line: 95, column: 16, scope: !110)
!128 = !DILocation(line: 95, column: 33, scope: !110)
!129 = !DILocation(line: 95, column: 31, scope: !110)
!130 = !DILocation(line: 95, column: 22, scope: !110)
!131 = !DILocalVariable(name: "cm1", scope: !110, file: !1, line: 96, type: !5)
!132 = !DILocation(line: 96, column: 16, scope: !110)
!133 = !DILocation(line: 96, column: 29, scope: !110)
!134 = !DILocation(line: 96, column: 28, scope: !110)
!135 = !DILocation(line: 96, column: 22, scope: !110)
!136 = !DILocalVariable(name: "w", scope: !110, file: !1, line: 97, type: !5)
!137 = !DILocation(line: 97, column: 16, scope: !110)
!138 = !DILocation(line: 97, column: 24, scope: !110)
!139 = !DILocation(line: 97, column: 22, scope: !110)
!140 = !DILocalVariable(name: "ar", scope: !110, file: !1, line: 98, type: !141)
!141 = !DICompositeType(tag: DW_TAG_array_type, baseType: !5, size: 192, elements: !142)
!142 = !{!143}
!143 = !DISubrange(count: 3)
!144 = !DILocation(line: 98, column: 16, scope: !110)
!145 = !DILocalVariable(name: "ai", scope: !110, file: !1, line: 98, type: !141)
!146 = !DILocation(line: 98, column: 23, scope: !110)
!147 = !DILocation(line: 100, column: 16, scope: !148)
!148 = distinct !DILexicalBlock(scope: !110, file: !1, line: 100, column: 9)
!149 = !DILocation(line: 100, column: 15, scope: !148)
!150 = !DILocation(line: 100, column: 20, scope: !151)
!151 = distinct !DILexicalBlock(scope: !148, file: !1, line: 100, column: 9)
!152 = !DILocation(line: 100, column: 24, scope: !151)
!153 = !DILocation(line: 100, column: 22, scope: !151)
!154 = !DILocation(line: 100, column: 9, scope: !148)
!155 = !DILocation(line: 102, column: 21, scope: !156)
!156 = distinct !DILexicalBlock(scope: !151, file: !1, line: 101, column: 9)
!157 = !DILocation(line: 102, column: 13, scope: !156)
!158 = !DILocation(line: 102, column: 19, scope: !156)
!159 = !DILocation(line: 103, column: 21, scope: !156)
!160 = !DILocation(line: 103, column: 13, scope: !156)
!161 = !DILocation(line: 103, column: 19, scope: !156)
!162 = !DILocation(line: 105, column: 21, scope: !156)
!163 = !DILocation(line: 105, column: 13, scope: !156)
!164 = !DILocation(line: 105, column: 19, scope: !156)
!165 = !DILocation(line: 106, column: 21, scope: !156)
!166 = !DILocation(line: 106, column: 13, scope: !156)
!167 = !DILocation(line: 106, column: 19, scope: !156)
!168 = !DILocation(line: 108, column: 21, scope: !169)
!169 = distinct !DILexicalBlock(scope: !156, file: !1, line: 108, column: 13)
!170 = !DILocation(line: 108, column: 20, scope: !169)
!171 = !DILocation(line: 108, column: 25, scope: !169)
!172 = !DILocation(line: 108, column: 19, scope: !169)
!173 = !DILocation(line: 108, column: 29, scope: !174)
!174 = distinct !DILexicalBlock(scope: !169, file: !1, line: 108, column: 13)
!175 = !DILocation(line: 108, column: 33, scope: !174)
!176 = !DILocation(line: 108, column: 31, scope: !174)
!177 = !DILocation(line: 108, column: 13, scope: !169)
!178 = !DILocation(line: 110, column: 25, scope: !179)
!179 = distinct !DILexicalBlock(scope: !174, file: !1, line: 109, column: 13)
!180 = !DILocation(line: 110, column: 27, scope: !179)
!181 = !DILocation(line: 110, column: 26, scope: !179)
!182 = !DILocation(line: 110, column: 35, scope: !179)
!183 = !DILocation(line: 110, column: 33, scope: !179)
!184 = !DILocation(line: 110, column: 17, scope: !179)
!185 = !DILocation(line: 110, column: 23, scope: !179)
!186 = !DILocation(line: 111, column: 25, scope: !179)
!187 = !DILocation(line: 111, column: 17, scope: !179)
!188 = !DILocation(line: 111, column: 23, scope: !179)
!189 = !DILocation(line: 112, column: 25, scope: !179)
!190 = !DILocation(line: 112, column: 17, scope: !179)
!191 = !DILocation(line: 112, column: 23, scope: !179)
!192 = !DILocation(line: 114, column: 25, scope: !179)
!193 = !DILocation(line: 114, column: 27, scope: !179)
!194 = !DILocation(line: 114, column: 26, scope: !179)
!195 = !DILocation(line: 114, column: 35, scope: !179)
!196 = !DILocation(line: 114, column: 33, scope: !179)
!197 = !DILocation(line: 114, column: 17, scope: !179)
!198 = !DILocation(line: 114, column: 23, scope: !179)
!199 = !DILocation(line: 115, column: 25, scope: !179)
!200 = !DILocation(line: 115, column: 17, scope: !179)
!201 = !DILocation(line: 115, column: 23, scope: !179)
!202 = !DILocation(line: 116, column: 25, scope: !179)
!203 = !DILocation(line: 116, column: 17, scope: !179)
!204 = !DILocation(line: 116, column: 23, scope: !179)
!205 = !DILocation(line: 118, column: 21, scope: !179)
!206 = !DILocation(line: 118, column: 25, scope: !179)
!207 = !DILocation(line: 118, column: 23, scope: !179)
!208 = !DILocation(line: 118, column: 19, scope: !179)
!209 = !DILocation(line: 119, column: 22, scope: !179)
!210 = !DILocation(line: 119, column: 28, scope: !179)
!211 = !DILocation(line: 119, column: 36, scope: !179)
!212 = !DILocation(line: 119, column: 27, scope: !179)
!213 = !DILocation(line: 119, column: 41, scope: !179)
!214 = !DILocation(line: 119, column: 47, scope: !179)
!215 = !DILocation(line: 119, column: 55, scope: !179)
!216 = !DILocation(line: 119, column: 46, scope: !179)
!217 = !DILocation(line: 119, column: 39, scope: !179)
!218 = !DILocation(line: 119, column: 20, scope: !179)
!219 = !DILocation(line: 120, column: 22, scope: !179)
!220 = !DILocation(line: 120, column: 28, scope: !179)
!221 = !DILocation(line: 120, column: 36, scope: !179)
!222 = !DILocation(line: 120, column: 27, scope: !179)
!223 = !DILocation(line: 120, column: 41, scope: !179)
!224 = !DILocation(line: 120, column: 47, scope: !179)
!225 = !DILocation(line: 120, column: 55, scope: !179)
!226 = !DILocation(line: 120, column: 46, scope: !179)
!227 = !DILocation(line: 120, column: 39, scope: !179)
!228 = !DILocation(line: 120, column: 20, scope: !179)
!229 = !DILocation(line: 122, column: 30, scope: !179)
!230 = !DILocation(line: 122, column: 38, scope: !179)
!231 = !DILocation(line: 122, column: 43, scope: !179)
!232 = !DILocation(line: 122, column: 41, scope: !179)
!233 = !DILocation(line: 122, column: 17, scope: !179)
!234 = !DILocation(line: 122, column: 25, scope: !179)
!235 = !DILocation(line: 122, column: 28, scope: !179)
!236 = !DILocation(line: 123, column: 30, scope: !179)
!237 = !DILocation(line: 123, column: 38, scope: !179)
!238 = !DILocation(line: 123, column: 43, scope: !179)
!239 = !DILocation(line: 123, column: 41, scope: !179)
!240 = !DILocation(line: 123, column: 17, scope: !179)
!241 = !DILocation(line: 123, column: 25, scope: !179)
!242 = !DILocation(line: 123, column: 28, scope: !179)
!243 = !DILocation(line: 125, column: 31, scope: !179)
!244 = !DILocation(line: 125, column: 17, scope: !179)
!245 = !DILocation(line: 125, column: 25, scope: !179)
!246 = !DILocation(line: 125, column: 28, scope: !179)
!247 = !DILocation(line: 126, column: 31, scope: !179)
!248 = !DILocation(line: 126, column: 17, scope: !179)
!249 = !DILocation(line: 126, column: 25, scope: !179)
!250 = !DILocation(line: 126, column: 28, scope: !179)
!251 = !DILocation(line: 127, column: 17, scope: !179)
!252 = !DILocation(line: 128, column: 13, scope: !179)
!253 = !DILocation(line: 108, column: 44, scope: !174)
!254 = !DILocation(line: 108, column: 49, scope: !174)
!255 = !DILocation(line: 108, column: 13, scope: !174)
!256 = distinct !{!256, !177, !257}
!257 = !DILocation(line: 128, column: 13, scope: !169)
!258 = !DILocation(line: 129, column: 9, scope: !156)
!259 = !DILocation(line: 130, column: 9, scope: !156)
!260 = !DILocation(line: 100, column: 41, scope: !151)
!261 = !DILocation(line: 100, column: 38, scope: !151)
!262 = !DILocation(line: 100, column: 9, scope: !151)
!263 = distinct !{!263, !154, !264}
!264 = !DILocation(line: 130, column: 9, scope: !148)
!265 = !DILocation(line: 132, column: 20, scope: !110)
!266 = !DILocation(line: 132, column: 18, scope: !110)
!267 = !DILocation(line: 133, column: 9, scope: !110)
!268 = !DILocation(line: 134, column: 5, scope: !110)
!269 = !DILocation(line: 90, column: 61, scope: !105)
!270 = !DILocation(line: 90, column: 5, scope: !105)
!271 = distinct !{!271, !108, !272}
!272 = !DILocation(line: 134, column: 5, scope: !102)
!273 = !DILocation(line: 140, column: 10, scope: !274)
!274 = distinct !DILexicalBlock(scope: !10, file: !1, line: 140, column: 10)
!275 = !DILocation(line: 140, column: 10, scope: !10)
!276 = !DILocalVariable(name: "denom", scope: !277, file: !1, line: 142, type: !5)
!277 = distinct !DILexicalBlock(scope: !274, file: !1, line: 141, column: 5)
!278 = !DILocation(line: 142, column: 16, scope: !277)
!279 = !DILocation(line: 142, column: 32, scope: !277)
!280 = !DILocation(line: 142, column: 24, scope: !277)
!281 = !DILocation(line: 144, column: 16, scope: !282)
!282 = distinct !DILexicalBlock(scope: !277, file: !1, line: 144, column: 9)
!283 = !DILocation(line: 144, column: 15, scope: !282)
!284 = !DILocation(line: 144, column: 20, scope: !285)
!285 = distinct !DILexicalBlock(scope: !282, file: !1, line: 144, column: 9)
!286 = !DILocation(line: 144, column: 24, scope: !285)
!287 = !DILocation(line: 144, column: 22, scope: !285)
!288 = !DILocation(line: 144, column: 9, scope: !282)
!289 = !DILocation(line: 146, column: 27, scope: !290)
!290 = distinct !DILexicalBlock(scope: !285, file: !1, line: 145, column: 9)
!291 = !DILocation(line: 146, column: 13, scope: !290)
!292 = !DILocation(line: 146, column: 21, scope: !290)
!293 = !DILocation(line: 146, column: 24, scope: !290)
!294 = !DILocation(line: 147, column: 27, scope: !290)
!295 = !DILocation(line: 147, column: 13, scope: !290)
!296 = !DILocation(line: 147, column: 21, scope: !290)
!297 = !DILocation(line: 147, column: 24, scope: !290)
!298 = !DILocation(line: 148, column: 13, scope: !290)
!299 = !DILocation(line: 149, column: 9, scope: !290)
!300 = !DILocation(line: 144, column: 37, scope: !285)
!301 = !DILocation(line: 144, column: 9, scope: !285)
!302 = distinct !{!302, !288, !303}
!303 = !DILocation(line: 149, column: 9, scope: !282)
!304 = !DILocation(line: 150, column: 5, scope: !277)
!305 = !DILocation(line: 151, column: 1, scope: !10)
!306 = distinct !DISubprogram(name: "CheckPointer", scope: !1, file: !1, line: 29, type: !307, isLocal: true, isDefinition: true, scopeLine: 30, flags: DIFlagPrototyped, isOptimized: false, unit: !0, variables: !2)
!307 = !DISubroutineType(types: !308)
!308 = !{null, !4, !309}
!309 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !310, size: 64)
!310 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!311 = !DILocalVariable(name: "p", arg: 1, scope: !306, file: !1, line: 29, type: !4)
!312 = !DILocation(line: 29, column: 34, scope: !306)
!313 = !DILocalVariable(name: "name", arg: 2, scope: !306, file: !1, line: 29, type: !309)
!314 = !DILocation(line: 29, column: 43, scope: !306)
!315 = !DILocation(line: 31, column: 10, scope: !316)
!316 = distinct !DILexicalBlock(scope: !306, file: !1, line: 31, column: 10)
!317 = !DILocation(line: 31, column: 12, scope: !316)
!318 = !DILocation(line: 31, column: 10, scope: !306)
!319 = !DILocation(line: 34, column: 9, scope: !320)
!320 = distinct !DILexicalBlock(scope: !316, file: !1, line: 32, column: 5)
!321 = !DILocation(line: 36, column: 1, scope: !306)
