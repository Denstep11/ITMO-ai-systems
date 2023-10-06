%ники игроков
nickname(foxx21).
nickname(cat1).
nickname(ard12).
nickname(denstep).
nickname(ypuzipy).
nickname(krluka).
nickname(professor).
nickname(patiant).
nickname(nagibator20012).

%список рангов
rank(silver1).
rank(silver2).
rank(silver3).
rank(silver4).
rank(silver5).
rank(silver6).
rank(nova1).
rank(nova2).
rank(nova3).
rank(nova4).
rank(kalash1).
rank(kalash2).
rank(kalash3).
rank(bigstar).
rank(supreme).

%реальное имя игроков
real_name(foxx21, andrey).
real_name(denstep, denis).
real_name(cat1, ivan).
real_name(professor, micha).
real_name(krluka, anna).
real_name(patiant, julia).
real_name(ard12, roman).
real_name(nagibator20012, artem).
real_name(ypuzipy, igor).

%ранги играков
player_rank(foxx21, nova3).
player_rank(cat1, nova3).
player_rank(ard12, silver5).
player_rank(denstep, kalash3).
player_rank(ypuzipy, kalash1).
player_rank(krluka, kalash3).
player_rank(professor, kalash3).
player_rank(patiant, bigstar).
player_rank(nagibator20012, silver6).

%игроки являющиеся друзьями
friend(foxx21, cat1).
friend(cat1, foxx21).
friend(denstep, ard12).
friend(ard12, denstep).
friend(professor, denstep).
friend(denstep, professor).

%проверка на одинаковость рангов играков
same_rank(X,Y) :- player_rank(X, R1), player_rank(Y, R2), rank(R1)==rank(R2).

%проверка могут ли игроки играть вместе
can_play_together(X,Y) :- friend(X,Y), same_rank(X,Y).

%с кем может играть игрок
can_play_with(X, Nickname) :- friend(X, Nick), same_rank(X,Nick), Nickname=Nick.

%потенциальные друзья
potential_friends(X, Nickname) :- nickname(Nick), same_rank(X, Nick), X\=Nick, Nickname=Nick.

%список реальных имен друзей
friends_real_name(X, Name) :- friend(X, Nick), real_name(Nick, Fname), Name=Fname.