#include <stdio.h>

int main() {
  FILE *infile = fopen("roms/BLINKY", "rb");
  int buf;
  for (int c = 0; c < 50; c++) {
    fread(&buf, 2, 1, infile);
    // op a b c
    char op = (buf >> 4) & 0xf;
    char a = buf & 0xf;
    char b = (buf >> 12) & 0xf;
    char c = (buf >> 8) & 0xf;
    int nnn = (a << 8) | (b << 4) | c;
    char kk = (b << 4) | c;

    switch (op) {
      case 0x0: // CLS, RET
      printf("RET");
      break;
      case 0x1: // JP
      printf("JP %x", nnn);
      break;
      case 0x2: // CALL
      printf("CALL %x", nnn);
      break;
      case 0x3: // SE
      printf("SE V%x, %x", a, kk);
      break;
      case 0x4: // SNE
      printf("SNE V%x, %x", a, kk);
      break;
      case 0x5: // SE
      printf("SE V%x, V%x", a, b);
      break;
      case 0x6: // LD
      printf("LD V%x, %x", a, kk);
      break;
      case 0x7: // ADD
      printf("ADD V%x, %x", a, kk);
      break;
      case 0x8: // LD, OR, AND, XOR, SUB, SHR, SUBN, SHL
      switch (c) {
        case 0x0:
        printf("LD V%x, V%x", a, b);
        break;
        case 0x1:
        printf("OR V%x, V%x", a, b);
        break;
        case 0x2:
        printf("AND V%x, V%x", a, b);
        break;
        case 0x3:
        printf("XOR V%x, V%x", a, b);
        break;
        case 0x4:
        printf("ADD V%x, V%x", a, b);
        break;
        case 0x5:
        printf("SUB V%x, V%x", a, b);
        break;
        case 0x6:
        printf("SHR V%x, V%x", a, b); // TODO: special
        break;
        case 0x7:
        printf("SUBN V%x, V%x", a, b);
        break;
        case 0xe:
        printf("SHL V%x, V%x", a, b);
        break;
      }
      break;
      case 0x9: // SNE
      printf("SNE V%x, V%x", a, b);
      break;
      case 0xA: // LD
      printf("LD I, %x", nnn);
      break;
      case 0xB: // JP
      printf("JP V0, %x", nnn);
      break;
      case 0xC:
      printf("RND V%x, %x", a, kk);
      break;
      case 0xD: // DRW
      printf("DRW V%x, V%x, %x", a, b, c);
      break;
      case 0xE: // SKP
      switch (c) {
        case 0xE:
        printf("SKP V%x", a);
        break;
        case 0x1:
        printf("SKNP V%x", a);
        break;
      }
      printf("SKP V%x", a);
      break;
      case 0xF: // LD, LD, ADD, LD, LD, LD
      switch (kk) {
        case 0x7:
        printf("LD V%x, DT", a);
        break;
        case 0xA:
        printf("LD V%x, K", a);
        break;
        case 0x15:
        printf("LD DT, V%x", a);
        break;
        case 0x18:
        printf("LD ST, V%x", a);
        break;
        case 0x1e:
        printf("ADD I, V%x", a);
        break;
        case 0x29:
        printf("LD F, V%x", a);
        break;
        case 0x33:
        printf("LD B, V%x", a);
        break;
        case 0x55:
        printf("LD [I], V%x", a);
        break;
        case 0x65:
        printf("LD V%x, [I]", a);
        break;
      }
      break;
    }
    printf("\n");
    //printf("%x %x %x %x\n", buf >> 12, (buf >> 8) & 0xf, (buf >> 4) & 0xf, buf & 0xf);
  }
}
