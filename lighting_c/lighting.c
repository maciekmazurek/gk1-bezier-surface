#include <math.h>
#include <stdint.h>

#define EXTRACT_R(c) ((float)((c>>16)&0xFF))
#define EXTRACT_G(c) ((float)((c>>8)&0xFF))
#define EXTRACT_B(c) ((float)((c)&0xFF))

typedef struct {
    float x, y, z;
} Vector3D;

typedef struct {
    Vector3D p;
    Vector3D n;
    float u, v;          // parametric coordinates
} Vertex;

typedef struct {
    Vertex v[3];
} Triangle;

// TODO: add vector V (eye position)
typedef struct {
    float kd, ks;
    int   m;
    float lx, ly, lz;
    float io_r, io_g, io_b;
    float il_r, il_g, il_b;
} LightingParams;

typedef struct {
    int width;
    int height;
    const uint32_t *pixels; // ARGB32 row-major
} Texture;

static inline void normalize(Vector3D *v) {
    float len = sqrtf(v->x*v->x + v->y*v->y + v->z*v->z);
    if (len > 1e-9f) {
        float inv = 1.0f/len;
        v->x *= inv; v->y *= inv; v->z *= inv;
    }
}

static inline void swap_vertices(Vertex *a, Vertex *b) {
    Vertex temp = *a;
    *a = *b;
    *b = temp;
}

static inline void sort_vertices(Triangle *T) {
    // Bubble sort of 3 vertices by y-coordinate
    if (T->v[0].p.y > T->v[1].p.y) swap_vertices(&T->v[0], &T->v[1]);
    if (T->v[0].p.y > T->v[2].p.y) swap_vertices(&T->v[0], &T->v[2]);
    if (T->v[1].p.y > T->v[2].p.y) swap_vertices(&T->v[1], &T->v[2]);
}

static inline void sample_texture(const Texture *T, float u, float v,
                              float *r, float *g, float *b) {
    if (u<0.f) u=0.f; if (u>1.f) u=1.f;
    if (v<0.f) v=0.f; if (v>1.f) v=1.f;
    float x = u * (T->width - 1);
    float y = v * (T->height - 1);
    int x0 = (int)x, y0 = (int)y;
    int x1 = (x0 + 1 < T->width) ? x0 + 1 : x0;
    int y1 = (y0 + 1 < T->height) ? y0 + 1 : y0;
    float fx = x - x0, fy = y - y0;

    const uint32_t *pix = T->pixels;
    uint32_t p00 = pix[y0 * T->width + x0];
    uint32_t p10 = pix[y0 * T->width + x1];
    uint32_t p01 = pix[y1 * T->width + x0];
    uint32_t p11 = pix[y1 * T->width + x1];

    float r0 = EXTRACT_R(p00)*(1-fx) + EXTRACT_R(p10)*fx;
    float r1 = EXTRACT_R(p01)*(1-fx) + EXTRACT_R(p11)*fx;
    *r = (r0*(1-fy) + r1*fy)/255.f;

    float g0 = EXTRACT_G(p00)*(1-fx) + EXTRACT_G(p10)*fx;
    float g1 = EXTRACT_G(p01)*(1-fx) + EXTRACT_G(p11)*fx;
    *g = (g0*(1-fy) + g1*fy)/255.f;

    float b0 = EXTRACT_B(p00)*(1-fx) + EXTRACT_B(p10)*fx;
    float b1 = EXTRACT_B(p01)*(1-fx) + EXTRACT_B(p11)*fx;
    *b = (b0*(1-fy) + b1*fy)/255.f;
}

static inline uint32_t shade_pixel(const Vector3D *pos,
                                   Vector3D n,
                                   float io_r, float io_g, float io_b,
                                   const LightingParams *P) {
    normalize(&n);
    Vector3D L = { P->lx - pos->x, P->ly - pos->y, P->lz - pos->z };
    normalize(&L);
    float cos_nl = n.x*L.x + n.y*L.y + n.z*L.z;
    float cos_vr = -1.f;
    if (cos_nl > 0.f) {
        Vector3D R = (Vector3D){ 2.f*cos_nl*n.x - L.x,
                                 2.f*cos_nl*n.y - L.y,
                                 2.f*cos_nl*n.z - L.z };
        normalize(&R);
        // Optimization simplification (we assume V = (0,0,-1))
        // Should be fixed when introducing a variable vector V
        cos_vr = -R.z;
    } else cos_nl = 0.f;

    float il_r = P->il_r, il_g = P->il_g, il_b = P->il_b;
    float diffuse_r = P->kd * il_r * io_r * cos_nl;
    float diffuse_g = P->kd * il_g * io_g * cos_nl;
    float diffuse_b = P->kd * il_b * io_b * cos_nl;

    float spec = (cos_vr > 0.f) ? P->ks * powf(cos_vr,(float)P->m) : 0.f;
    float spec_r = spec * il_r * io_r;
    float spec_g = spec * il_g * io_g;
    float spec_b = spec * il_b * io_b;

    float r = diffuse_r + spec_r; if (r>1.f) r=1.f;
    float g = diffuse_g + spec_g; if (g>1.f) g=1.f;
    float b = diffuse_b + spec_b; if (b>1.f) b=1.f;

    return 0xFF000000u | ((uint32_t)(r*255.f)<<16) | ((uint32_t)(g*255.f)<<8) | (uint32_t)(b*255.f);
}

static void fill_triangle(Triangle *T, const LightingParams *P,
                          uint32_t *framebuffer, int W, int H,
                          int off_x, int off_y, const Texture *texture) {
    sort_vertices(T);
    // Rozpakowanie
    float x0=T->v[0].p.x, y0=T->v[0].p.y, z0=T->v[0].p.z;
    float nx0=T->v[0].n.x, ny0=T->v[0].n.y, nz0=T->v[0].n.z;
    float u0=T->v[0].u, v0=T->v[0].v;

    float x1=T->v[1].p.x, y1=T->v[1].p.y, z1=T->v[1].p.z;
    float nx1=T->v[1].n.x, ny1=T->v[1].n.y, nz1=T->v[1].n.z;
    float u1=T->v[1].u, v1=T->v[1].v;

    float x2=T->v[2].p.x, y2=T->v[2].p.y, z2=T->v[2].p.z;
    float nx2=T->v[2].n.x, ny2=T->v[2].n.y, nz2=T->v[2].n.z;
    float u2=T->v[2].u, v2=T->v[2].v;

    float dy02 = y2 - y0; if (fabsf(dy02)<1e-6f) return;
    float denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2);
    if (fabsf(denom)<1e-12f) return;

    float inv_m02=(x2-x0)/dy02;
    float dy01=y1-y0, inv_m01=(fabsf(dy01)>=1e-6f)?(x1-x0)/dy01:0.f;
    float dy12=y2-y1, inv_m12=(fabsf(dy12)>=1e-6f)?(x2-x1)/dy12:0.f;

    int y_start=(int)ceilf(y0), y_end=(int)ceilf(y2);
    for(int yi=y_start; yi<y_end; ++yi){
        float y=(float)yi;
        if (y<y0 || y>=y2) continue;
        float x_long = x0 + (y - y0)*inv_m02;
        float x_short = (y < y1)
            ? (fabsf(dy01)<1e-6f ? x_long : x0 + (y - y0)*inv_m01)
            : (fabsf(dy12)<1e-6f ? x_long : x1 + (y - y1)*inv_m12);

        float xl=x_long, xr=x_short;
        if (xl>xr){ float tmp=xl; xl=xr; xr=tmp; }

        int xs=(int)ceilf(xl), xe=(int)ceilf(xr);
        for(int xi=xs; xi<xe; ++xi){
            float w0=((y1 - y2)*(xi - x2) + (x2 - x1)*(y - y2))/denom;
            float w1=((y2 - y0)*(xi - x2) + (x0 - x2)*(y - y2))/denom;
            float w2=1.f - w0 - w1;
            if (w0<0.f||w1<0.f||w2<0.f) continue;

            Vector3D pos = {
                w0*x0 + w1*x1 + w2*x2,
                w0*y0 + w1*y1 + w2*y2,
                w0*z0 + w1*z1 + w2*z2
            };
            Vector3D n = {
                w0*nx0 + w1*nx1 + w2*nx2,
                w0*ny0 + w1*ny1 + w2*ny2,
                w0*nz0 + w1*nz1 + w2*nz2
            };
            float u = w0*u0 + w1*u1 + w2*u2;
            float v = w0*v0 + w1*v1 + w2*v2;

            float io_r=P->io_r, io_g=P->io_g, io_b=P->io_b;
            if (texture){
                sample_texture(texture, u, v, &io_r, &io_g, &io_b);
            }

            uint32_t color = shade_pixel(&pos, n, io_r, io_g, io_b, P);
            int sx=xi+off_x, sy=off_y - yi;
            if (sx>=0 && sx<W && sy>=0 && sy<H)
                framebuffer[sy*W + sx] = color;
        }
    }
}

void fill_surface(Triangle *tris, int tri_count,
                  const LightingParams *params,
                  uint32_t *framebuffer, int W, int H,
                  int off_x, int off_y, const Texture *texture){
    for(int i=0;i<tri_count;++i)
        fill_triangle(&tris[i], params, framebuffer, W, H, off_x, off_y, texture);
}