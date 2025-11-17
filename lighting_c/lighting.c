#include <math.h>
#include <stdint.h>

typedef struct {
    float x, y, z;
} Vector3D;

typedef struct {
    Vector3D p;
    Vector3D n;
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

static inline void normalize(Vector3D *v) {
    float len = sqrtf(v->x*v->x + v->y*v->y + v->z*v->z);
    if (len > 1e-9f) {
        float inv = 1.0f/len;
        v->x *= inv; v->y *= inv; v->z *= inv;
    }
}

static inline void swapVertices(Vertex *a, Vertex *b) {
    Vertex temp = *a;
    *a = *b;
    *b = temp;
}

static inline void sortVertices(Triangle *T) {
    if (T->v[0].p.y > T->v[1].p.y) {
        swapVertices(&T->v[0], &T->v[1]);
    }
    if (T->v[0].p.y > T->v[2].p.y) {
        swapVertices(&T->v[0], &T->v[2]);
    }
    if (T->v[1].p.y > T->v[2].p.y) {
        swapVertices(&T->v[1], &T->v[2]);
    }
}

static inline uint32_t shade_pixel(const Vector3D *pos,
                                   Vector3D n,
                                   const LightingParams *P) {
    normalize(&n);
    Vector3D L = {
        P->lx - pos->x, 
        P->ly - pos->y, 
        P->lz - pos->z 
    };
    normalize(&L);

    float cos_nl = n.x*L.x + n.y*L.y + n.z*L.z;
    if (cos_nl < 0.f) cos_nl = 0.f;

    float kd_cos_nl = P->kd * cos_nl;
    float diffuse_r = kd_cos_nl * P->il_r * P->io_r;
    float diffuse_g = kd_cos_nl * P->il_g * P->io_g;
    float diffuse_b = kd_cos_nl * P->il_b * P->io_b;

    Vector3D R = {
        2.f*cos_nl*n.x - L.x,
        2.f*cos_nl*n.y - L.y,
        2.f*cos_nl*n.z - L.z
    };
    normalize(&R);

    float cos_vr = R.z;
    if (cos_vr < 0.f) cos_vr = 0.f;

    float ks_cos_m_vr = (cos_vr>0.f) ? P->ks * powf(cos_vr,(float)P->m) : 0.f;
    float specular_r = ks_cos_m_vr * P->il_r * P->io_r;
    float specular_g = ks_cos_m_vr * P->il_g * P->io_g;
    float specular_b = ks_cos_m_vr * P->il_b * P->io_b;

    float r = diffuse_r + specular_r;
    float g = diffuse_g + specular_g;
    float b = diffuse_b + specular_b;

    if (r > 1.f) r = 1.f;
    if (g > 1.f) g = 1.f;
    if (b > 1.f) b = 1.f;

    return 0xFF000000u | ((uint32_t)(r*255.f)<<16) | ((uint32_t)(g*255.f)<<8) | (uint32_t)(b*255.f);
}

static void fill_triangle(Triangle *T,
                          const LightingParams *P,
                          uint32_t *framebuffer, int W, int H,
                          int off_x, int off_y) {
    // Sortowanie wierzchołków rosnąco wg y
    sortVertices(T);

    // Rozpakowanie do lokalnych (kopie – 6 floatów jak wcześniej)
    float x0=T->v[0].p.x, y0=T->v[0].p.y, z0=T->v[0].p.z;
    float nx0=T->v[0].n.x, ny0=T->v[0].n.y, nz0=T->v[0].n.z;
    float x1=T->v[1].p.x, y1=T->v[1].p.y, z1=T->v[1].p.z;
    float nx1=T->v[1].n.x, ny1=T->v[1].n.y, nz1=T->v[1].n.z;
    float x2=T->v[2].p.x, y2=T->v[2].p.y, z2=T->v[2].p.z;
    float nx2=T->v[2].n.x, ny2=T->v[2].n.y, nz2=T->v[2].n.z;

    float dy02 = y2 - y0;
    if (fabsf(dy02) < 1e-6f) return;
    float denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2);
    if (fabsf(denom) < 1e-12f) return;

    float inv_m02 = (x2 - x0) / dy02;
    float dy01 = y1 - y0, inv_m01 = (fabsf(dy01)>=1e-6f)?(x1 - x0)/dy01:0.f;
    float dy12 = y2 - y1, inv_m12 = (fabsf(dy12)>=1e-6f)?(x2 - x1)/dy12:0.f;

    int y_start = (int)ceilf(y0);
    int y_end   = (int)ceilf(y2);
    for (int yi=y_start; yi<y_end; ++yi) {
        float y = (float)yi;
        if (y < y0 || y >= y2) continue;

        float x_long = x0 + (y - y0)*inv_m02;
        float x_short = (y < y1)
            ? (fabsf(dy01)<1e-6f ? x_long : x0 + (y - y0)*inv_m01)
            : (fabsf(dy12)<1e-6f ? x_long : x1 + (y - y1)*inv_m12);

        float xl = x_long, xr = x_short;
        if (xl > xr) { float tmp=xl; xl=xr; xr=tmp; }

        int xs = (int)ceilf(xl);
        int xe = (int)ceilf(xr);
        for (int xi=xs; xi<xe; ++xi) {
            float w0 = ((y1 - y2)*(xi - x2) + (x2 - x1)*(y - y2)) / denom;
            float w1 = ((y2 - y0)*(xi - x2) + (x0 - x2)*(y - y2)) / denom;
            float w2 = 1.f - w0 - w1;
            if (w0<0.f || w1<0.f || w2<0.f) continue;

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

            uint32_t color = shade_pixel(&pos, n, P);
            int sx = xi + off_x;
            int sy = off_y - yi;
            if (sx>=0 && sx<W && sy>=0 && sy<H)
                framebuffer[sy*W + sx] = color;
        }
    }
}

void fill_surface(Triangle *tris, int tri_count,
                  const LightingParams *params,
                  uint32_t *framebuffer, int W, int H,
                  int off_x, int off_y) {
    for (int i=0;i<tri_count;++i)
        fill_triangle(&tris[i], params, framebuffer, W, H, off_x, off_y);
}