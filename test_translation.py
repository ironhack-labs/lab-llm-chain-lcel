import unittest
from fastapi.testclient import TestClient
from translation import build_chain, prompt_template
from serve import create_app

class TranslationTests(unittest.TestCase):
    def test_prompt(self):
        result = prompt_template.invoke({'language':'italian','text':'My tailor is rich'}).to_messages()
        self.assertEqual(result[0].type, 'system')
        self.assertEqual(result[1].content, 'My tailor is rich')
    def test_chain_batch(self):
        chain = build_chain('offline')
        result = chain.batch([{'language':lang,'text':'Good evening, how are you?'} for lang in ['italian','french']])
        self.assertEqual(result, ['Buonasera, come stai?', 'Bonsoir, comment vas-tu ?'])
    def test_stream(self):
        self.assertEqual(''.join(build_chain('offline').stream({'language':'italian','text':'My tailor is rich'})), 'Il mio sarto è ricco.')
    def test_unsupported_offline(self):
        with self.assertRaises(ValueError): build_chain('offline').invoke({'language':'italian','text':'unknown'})
    def test_api(self):
        with TestClient(create_app('offline')) as client:
            response = client.post('/chain/invoke', json={'input':{'language':'italian','text':'Good evening, how are you?'}})
            self.assertEqual(response.status_code,200, response.text)
            self.assertEqual(response.json()['output'],'Buonasera, come stai?')
            self.assertEqual(client.get('/chain/input_schema').status_code,200)
            self.assertEqual(client.get('/chain/playground/').status_code,200)
            self.assertEqual(client.post('/chain/invoke',json={'input':{'language':'italian','text':''}}).status_code,422)
if __name__ == '__main__': unittest.main()
