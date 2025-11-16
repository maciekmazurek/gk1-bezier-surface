#include <math.h>
#include <stdint.h>

// Struktura dla trójkąta (spłaszczone dane)
typedef struct {
    float x, y, z;      // Pozycja
    float nx, ny, nz;   // Normalna
} Vertex;

// Funkcja normalizacji wektora
static inline void normalize(float *x, float *y, float *z) {
    float len = sqrtf((*x)*(*x) + (*y)*(*y) + (*z)*(*z));
    if (len > 1e-9f) {
        *x /= len;
        *y /= len;
        *z /= len;
    }
}

// Clamp do [0, 1]
static inline float clamp(float val) {
    if (val < 0.0f) return 0.0f;
    if (val > 1.0f) return 1.0f;
    return val;
}

// Obliczenie oświetlenia dla pojedynczego piksela
static void compute_lighting(
    float nx, float ny, float nz,
    float px, float py, float pz,
    float lx, float ly, float lz,
    float kd, float ks, int m,
    float io_r, float io_g, float io_b,
    float il_r, float il_g, float il_b,
    uint8_t *out_r, uint8_t *out_g, uint8_t *out_b
) {
    // Normalizuj normalną
    normalize(&nx, &ny, &nz);
    
    // Wektor do światła L
    float lx_dir = lx - px;
    float ly_dir = ly - py;
    float lz_dir = lz - pz;
    normalize(&lx_dir, &ly_dir, &lz_dir);
    
    // cos(N, L)
    float cos_nl = nx * lx_dir + ny * ly_dir + nz * lz_dir;
    if (cos_nl < 0.0f) cos_nl = 0.0f;
    
    // Diffuse
    float diff_r = kd * il_r * io_r * cos_nl;
    float diff_g = kd * il_g * io_g * cos_nl;
    float diff_b = kd * il_b * io_b * cos_nl;
    
    // Odbity wektor R = 2<N,L>N - L
    float dot_2nl = 2.0f * cos_nl;
    float rx = dot_2nl * nx - lx_dir;
    float ry = dot_2nl * ny - ly_dir;
    float rz = dot_2nl * nz - lz_dir;
    normalize(&rx, &ry, &rz);
    
    // V = [0, 0, 1]
    float vx = 0.0f, vy = 0.0f, vz = 1.0f;
    
    // cos(V, R)
    float cos_vr = vx * rx + vy * ry + vz * rz;
    if (cos_vr < 0.0f) cos_vr = 0.0f;
    
    // Specular (cos^m)
    float spec_factor = powf(cos_vr, (float)m);
    float spec_r = ks * il_r * io_r * spec_factor;
    float spec_g = ks * il_g * io_g * spec_factor;
    float spec_b = ks * il_b * io_b * spec_factor;
    
    // Suma + clamp
    float final_r = clamp(diff_r + spec_r);
    float final_g = clamp(diff_g + spec_g);
    float final_b = clamp(diff_b + spec_b);
    
    // Konwersja do [0, 255]
    *out_r = (uint8_t)(final_r * 255.0f);
    *out_g = (uint8_t)(final_g * 255.0f);
    *out_b = (uint8_t)(final_b * 255.0f);
}

// Funkcja scanline dla trójkąta (uproszczona wersja)
// W pełnej wersji zaimplementuj swój algorytm scanline_filling
static void fill_triangle(
    float x0, float y0, float z0, float nx0, float ny0, float nz0,
    float x1, float y1, float z1, float nx1, float ny1, float nz1,
    float x2, float y2, float z2, float nx2, float ny2, float nz2,
    float kd, float ks, int m,
    float lx, float ly, float lz,
    float io_r, float io_g, float io_b,
    float il_r, float il_g, float il_b,
    uint32_t *framebuffer, int img_w, int img_h,
    int offset_x, int offset_y
) {
    // Sortowanie po Y (v0 najwyżej, v2 najniżej)
    // Używamy prostych zamian; liczba wierzchołków = 3
    if (y0 > y1) {
        float tx=x0, ty=y0, tz=z0, tnx=nx0, tny=ny0, tnz=nz0;
        x0=x1; y0=y1; z0=z1; nx0=nx1; ny0=ny1; nz0=nz1;
        x1=tx; y1=ty; z1=tz; nx1=tnx; ny1=tny; nz1=tnz;
    }
    if (y0 > y2) {
        float tx=x0, ty=y0, tz=z0, tnx=nx0, tny=ny0, tnz=nz0;
        x0=x2; y0=y2; z0=z2; nx0=nx2; ny0=ny2; nz0=nz2;
        x2=tx; y2=ty; z2=tz; nx2=tnx; ny2=tny; nz2=tnz;
    }
    if (y1 > y2) {
        float tx=x1, ty=y1, tz=z1, tnx=nx1, tny=ny1, tnz=nz1;
        x1=x2; y1=y2; z1=z2; nx1=nx2; ny1=ny2; nz1=nz2;
        x2=tx; y2=ty; z2=tz; nx2=tnx; ny2=tny; nz2=tnz;
    }

    // Sprawdzenie degeneracji (prawie poziome albo wspólne y)
    float dy02 = y2 - y0;
    if (fabsf(dy02) < 1e-6f) return;

    // Barycentric denominator (używany do testu wnętrza oraz interpolacji)
    float denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2);
    if (fabsf(denom) < 1e-12f) return;

    // Długa krawędź v0->v2
    float dx02 = x2 - x0;
    float inv_m02 = dx02 / dy02; // 1/m (przyrost x na jednostkę y)

    // Górna część: v0->v1 oraz v0->v2
    float dy01 = y1 - y0;
    float inv_m01 = 0.0f;
    if (fabsf(dy01) >= 1e-6f)
        inv_m01 = (x1 - x0) / dy01;

    // Dolna część: v1->v2 oraz v0->v2
    float dy12 = y2 - y1;
    float inv_m12 = 0.0f;
    if (fabsf(dy12) >= 1e-6f)
        inv_m12 = (x2 - x1) / dy12;

    // Zakres scanline (half-open na górze: [ceil(y0), ceil(y2)))
    int y_start = (int)ceilf(y0);
    int y_end   = (int)ceilf(y2); // exclusive

    for (int y = y_start; y < y_end; ++y) {
        float yf = (float)y + 0.0f; // używamy całkowitych scanline jak w Pythonie

        // Pomiń scanline powyżej lub poniżej zakresu segmentów
        if (yf < y0 || yf >= y2) continue;

        // x na długiej krawędzi
        float x_long = x0 + (yf - y0) * inv_m02;

        // Wybór krótkiej krawędzi (górna lub dolna połowa)
        float x_short;
        if (yf < y1) {
            // Górna połowa
            if (fabsf(dy01) < 1e-6f) continue; // brak górnej części
            x_short = x0 + (yf - y0) * inv_m01;
        } else {
            // Dolna połowa
            if (fabsf(dy12) < 1e-6f) continue; // brak dolnej części
            x_short = x1 + (yf - y1) * inv_m12;
        }

        float x_left = x_long;
        float x_right = x_short;
        if (x_left > x_right) {
            float tmp = x_left; x_left = x_right; x_right = tmp;
        }

        int x_start = (int)ceilf(x_left);
        int x_end   = (int)ceilf(x_right); // exclusive
        for (int x = x_start; x < x_end; ++x) {
            // Barycentric weights (dla punktu (x, yf))
            float w0 = ((y1 - y2) * (x - x2) + (x2 - x1) * (yf - y2)) / denom;
            float w1 = ((y2 - y0) * (x - x2) + (x0 - x2) * (yf - y2)) / denom;
            float w2 = 1.0f - w0 - w1;

            // Test wnętrza
            if (w0 < 0.0f || w1 < 0.0f || w2 < 0.0f) continue;

            // Interpolacja normalnej i pozycji (z + xy dla compute_lighting)
            float nx = w0*nx0 + w1*nx1 + w2*nx2;
            float ny = w0*ny0 + w1*ny1 + w2*ny2;
            float nz = w0*nz0 + w1*nz1 + w2*nz2;

            float z  = w0*z0  + w1*z1  + w2*z2;
            float px = w0*x0  + w1*x1  + w2*x2; // (również można użyć x, ale zachowujemy spójność)
            float py = w0*y0  + w1*y1  + w2*y2;

            // Oświetlenie
            uint8_t r, g, b;
            compute_lighting(nx, ny, nz, px, py, z,
                             lx, ly, lz, kd, ks, m,
                             io_r, io_g, io_b,
                             il_r, il_g, il_b,
                             &r, &g, &b);

            // Transformacja do bufora ekranu
            int xi = x + offset_x;
            int yi = offset_y - y; // odwrócenie osi Y jak wcześniej

            if (xi >= 0 && xi < img_w && yi >= 0 && yi < img_h) {
                framebuffer[yi * img_w + xi] = 0xFF000000u | ((uint32_t)r << 16) | ((uint32_t)g << 8) | (uint32_t)b;
            }
        }
    }
}

// Główna funkcja wywoływana z Pythona
void fill_surface(
    float *triangles,    // Tablica: [x0,y0,z0,nx0,ny0,nz0, x1,y1,z1,nx1,ny1,nz1, ...]
    int tri_count,
    float kd, float ks, int m,
    float lx, float ly, float lz,
    float io_r, float io_g, float io_b,
    float il_r, float il_g, float il_b,
    uint32_t *img_ptr,
    int img_w, int img_h,
    int offset_x, int offset_y
) {
    for (int i = 0; i < tri_count; i++) {
        float *tri = &triangles[i * 18];  // 3 wierzchołki × 6 floatów
        
        fill_triangle(
            tri[0], tri[1], tri[2], tri[3], tri[4], tri[5],      // v0
            tri[6], tri[7], tri[8], tri[9], tri[10], tri[11],    // v1
            tri[12], tri[13], tri[14], tri[15], tri[16], tri[17], // v2
            kd, ks, m, lx, ly, lz,
            io_r, io_g, io_b, il_r, il_g, il_b,
            img_ptr, img_w, img_h, offset_x, offset_y
        );
    }
}