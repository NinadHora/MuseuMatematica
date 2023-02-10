# MuseuMatematica
Projeto da disciplina inf1407 da PUC RIo com o objetivo de colocar em pratica as teorias da sala de Aula. Site ficticio que simula um museu da matemática.

#ideia Inicial 

Museu da Matemática é um museu situado no rio de janeiro que tem exposicoes presenciais e um site com repositorio online das exposicoes e historias compartilhadas no museu. 

Escopo do Trabalho
 O site tem informacoes sobre o museu e exposições
 Duas views com cenarios diferentes : View do visitante e view do administrador do museu, na view de reservas de exposições há views diferentes para admin e usuario comum. O admin pode ver todas as reservas feitas por todos os usuarios, os visitantes so ve as deles. Assim como suas reservas.
 Operacoes do CRUD: Criamos os registros, Fizemos leituras dos registros para exibição no site, implementação de edição das reservas na view visitante e na view admin, e deletar informações. So o admin pode editar, excluir e adicionar uma exposicao. O usuario comum so pode reservar.
 Utilizamos sqlite
 Site em python, django, html, css e javascript
 Aspectos de segurança das informações : Controle de acesso das informações -> quais as informações disponiveis para visitantes e para administrador do site e como eles leem as informacoes contidas na base de dados esta explicito nas views de reservas de exposicoes e na exposicao.
 Fizemos commits semanais.

Implementamos um ajax que verifica se o horario de entrada de uma reserva em uma exposicao é igual ao horario de saida.

site publicado: https://museumatematica-production.up.railway.app/
