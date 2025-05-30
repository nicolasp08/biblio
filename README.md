# biblio
EXERCICE 4

 """
    Service fournissant la logique métier pour la gestion des emprunts de livres dans un système de bibliothèque.
    Ce service gère la création, la récupération, la prolongation et le retour des emprunts, en appliquant des règles telles que le statut de l'utilisateur, la disponibilité des livres, la limite d'emprunts et la vérification des retards.

    Méthodes
    --------
    __init__(loan_repository, book_repository, user_repository)
        Initialise le LoanService avec les repositories pour les emprunts, les livres et les utilisateurs.
    get_active_loans() -> List[Loan]
        Récupère tous les emprunts actifs (non encore retournés).
    get_overdue_loans() -> List[Loan]
        Récupère tous les emprunts en retard.
    get_loans_by_user(*, user_id: int) -> List[Loan]
        Récupère tous les emprunts d'un utilisateur spécifique.
    get_loans_by_book(*, book_id: int) -> List[Loan]
        Récupère tous les emprunts d'un livre spécifique.
    create_loan(*, user_id: int, book_id: int, loan_period_days: int = 14) -> Loan
        Crée un nouvel emprunt après vérification du statut de l'utilisateur et du livre, des limites d'emprunt et des règles métier.
    return_loan(*, loan_id: int) -> Loan
        Marque un emprunt comme retourné et met à jour la quantité disponible du livre.
    extend_loan(*, loan_id: int, extension_days: int = 7) -> Loan
        Prolonge la date d'échéance d'un emprunt, en appliquant les règles sur les retards et les limites de prolongation.
    """

    EXERCICE 5
    
    CREATION DE ROUTES POUR UTILISER L API

    POUR LE SERVICE BOOKS

from sqlalchemy.orm import Session
from typing import List

from .base import BaseRepository
from ..models.books import Book


class BookRepository(BaseRepository[Book, None, None]):
    def get_by_isbn(self, db: Session, *, isbn: str) -> Book:
        """
        Récupère un livre par son ISBN.
        """
        return db.query(Book).filter(Book.isbn == isbn).first()

    def get_by_title(self, db: Session, *, title: str) -> List[Book]:
        """
        Récupère des livres par leur titre (recherche partielle).
        """
        return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    def get_by_author(self, db: Session, *, author: str) -> List[Book]:
        """
        Récupère des livres par leur auteur (recherche partielle).
        """
        return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()


EXERCICE 6

MISE A JOUR DES DEPENDANCES

   """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.
    Décode le token JWT, valide sa charge utile et récupère l'utilisateur correspondant depuis la base de données.
    Lève des exceptions HTTP si le token est invalide ou si l'utilisateur n'existe pas.
    Args:
        db (Session): Session de base de données SQLAlchemy.
        token (str): Token JWT extrait de la requête.
    Returns:
        User: L'objet utilisateur authentifié.
    Raises:
        HTTPException: Si le token est invalide ou si l'utilisateur n'est pas trouvé.
    """
    """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.
    """
