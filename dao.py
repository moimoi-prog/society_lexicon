# ①必要なモジュールをインポート
import sqlalchemy.ext.declarative
import sqlalchemy.orm


# クラス
class Dao(object):
    # メタクラスの生成
    Base = sqlalchemy.ext.declarative.declarative_base()

    # テーブル: Task用クラス
    class Lexicons(Base):
        __tablename__ = "lexicon"
        id = sqlalchemy.Column(
            sqlalchemy.Integer, primary_key=True, autoincrement=True
        )

        title = sqlalchemy.Column(
            sqlalchemy.String(30)
        )

        template = sqlalchemy.Column(
            sqlalchemy.String(200)
        )

        advice = sqlalchemy.Column(
            sqlalchemy.String(200)
        )

    # コンストラクタ
    def __init__(self):
        # エンジンの生成
        self.engine = sqlalchemy.create_engine("mysql+pymysql://root:@127.0.0.1/example_db")

        # 定義したテーブル情報をDBと紐付ける(紐づくテーブルがない場合、生成される。)
        self.Base.metadata.create_all(self.engine)

        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = Session()

    # レコード一覧を取得する
    def get(self):
        return self.session.query(self.Lexicons).all()

    # 語句で検索()
    def search_title(self, title):
        return self.session.query(self.Lexicons).filter(self.Lexicons.title.like('%\\' + title + '%', escape='\\')).all()

    # idで検索()
    def search_id(self, id):
        return self.session.query(self.Lexicons).filter_by(id=id).first()

    # データを登録する
    def add(self):
        lexicon1 = self.Lexicons(title="新入社員挨拶", template="初めまして。〇〇〇〇と申します。社会人生活、全力で頑張ります。よろしくお願いします。", advice="できるだけ大きい声でハキハキと、聞いてくれる人の目を見て。")
        lexicon2 = self.Lexicons(title="志望動機:(情報系)", template="", advice="")
        lexicon3 = self.Lexicons(title="学生時代頑張ったこと", template="", advice="")
        self.session.add(lexicon1)
        self.session.add(lexicon2)
        self.session.add(lexicon3)
        self.session.commit()

    # データを削除する
    def delete(self, id):
        lexicon = self.session.query(self.Lexicons).filter_by(id=id).first()
        self.session.delete(lexicon)
        self.session.commit()


