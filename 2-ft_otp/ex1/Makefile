NAME = ft_otp
SRC = ft_otp.py

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