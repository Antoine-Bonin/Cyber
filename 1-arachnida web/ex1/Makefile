NAME = spider
SRC = spider.py

all: $(NAME)

$(NAME): $(SRC)
	cp $(SRC) $(NAME)
	chmod +x $(NAME)

clean:
	rm -f $(NAME)

fclean: clean
	rm -rf data/

re: fclean all

.PHONY: all clean fclean re