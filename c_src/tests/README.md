# Learn2Slither - C Test Suite

Comprehensive test suite para o motor de jogo em C.

## Estrutura

```
c_src/tests/
├── tests.h                      # Header com macros e interfaces
├── test_board_creation.c        # Testes de criação/destruição (5 funcs)
├── test_board_edge_cases.c      # Testes de edge cases (5 funcs)
├── test_board_validation.c      # Testes de validação (5 funcs)
├── test_board_memory.c          # Testes de memória/stress (5 funcs)
├── test_runner.c                # Main e coordenação (1 func)
└── Makefile                     # Compilação dos testes
```

## Executar Testes

### Testes normais
```bash
cd c_src/tests && make test
```

### Com Valgrind (detecção de memory leaks)
```bash
cd c_src/tests && make valgrind
```

### Limpar artefatos
```bash
cd c_src/tests && make clean   # Remove objetos
cd c_src/tests && make fclean  # Remove executável
```

## Cobertura de Testes

### Test: Board Creation (4 testes)
- ✅ Criar board com tamanho 10
- ✅ Destruir board corretamente
- ✅ Criar com tamanho máximo (20)
- ✅ Criar com tamanho mínimo (8)

### Test: Edge Cases (4 testes)
- ✅ Size muito pequeno (< 8) → defaults para 10
- ✅ Size muito grande (> 20) → defaults para 10
- ✅ Size negativo → defaults para 10
- ✅ Size zero → defaults para 10

### Test: Board Validation (4 testes)
- ✅ Snake inicializada corretamente
- ✅ Apples count correto (2 green, 1 red para size 10)
- ✅ Board reset funciona
- ✅ Game não está "over" inicialmente

### Test: Memory & Stress (4 testes)
- ✅ Multiple create/destroy (100 iterações) → sem leaks
- ✅ Destruir board NULL (seguro)
- ✅ Alocação de múltiplos tamanhos
- ✅ Consistência de estado

## Conformidade 42 Norminette

✅ Máximo 5 funções por arquivo
✅ Máximo 25 linhas por função
✅ Máximo 4 variáveis por função
✅ Headers 42 em todos os arquivos
✅ Sem warnings (-Wall -Wextra -Werror)

## Resultado Valgrind

```
==14680== HEAP SUMMARY:
==14680==     in use at exit: 0 bytes in 0 blocks
==14680==   total heap usage: 2,767 allocs, 2,767 frees
==14680== 
==14680== All heap blocks were freed -- no leaks are possible
==14680== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

✅ **Sem memory leaks**
✅ **Sem segmentation faults**
✅ **Todos os 16 testes passam**

## Macros de Teste

```c
// Assertion simples
ASSERT(condition, "mensagem de erro")

// Assertion com comparação de igualdade
ASSERT_EQ(actual, expected, "mensagem")

// Correr um teste (incrementa counters automaticamente)
RUN_TEST("nome do teste", test_function)
```

## Como Adicionar Novo Teste

1. Criar função `static bool test_something(void)`
2. Usar `ASSERT` ou `ASSERT_EQ` para validações
3. Adicionar ao struct `t_test_result` no runner
4. Chamar `RUN_TEST("nome", test_something)` no runner

Exemplo:
```c
static bool test_example(void)
{
    Board *board = board_create(10);
    ASSERT(board != NULL, "Alocação falhou");
    ASSERT_EQ(board->size, 10, "Tamanho incorreto");
    board_destroy(board);
    return (true);
}
```
