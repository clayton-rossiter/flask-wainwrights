import json

from .framework import Framework



class TestHTTPProtocols(Framework):
    """unittest to test GET/POST/PUT/PATCH/DELETE"""
    
    def setUp(self):
        super().setUp()
        self.url = "/fell/" + self.id

    def test_200_if_get(self):
        """ensure 200 status code is raised if using GET protocol"""
        r = self.app.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_405_if_put(self):
        """ensure 405 status code is raised if using PUT protocol"""
        r = self.app.put(self.url)
        self.assertEqual(r.status_code, 405)

    def test_405_if_post(self):
        """ensure 405 status code is raised if using PUT protocol"""
        r = self.app.post(self.url)
        self.assertEqual(r.status_code, 405)

    def test_405_if_delete(self):
        """ensure 405 status code is raised if using PUT protocol"""
        r = self.app.delete(self.url)
        self.assertEqual(r.status_code, 405)

    def test_405_if_patch(self):
        """ensure 405 status code is raised if using PUT protocol"""
        r = self.app.patch(self.url)
        self.assertEqual(r.status_code, 405)


class FellTest(Framework):
    """unittest for the fell/ endpoint"""

    def setUp(self):
        super().setUp()
        self.url = "/fell/"

    def test_404_if_no_id_provided(self):
        """expect 404 status code if no id is provided"""
        r = self.app.get(self.url)
        self.assertEqual(r.status_code, 404)
    
    def test_404_if_id_is_not_int(self):
        """tests robustness of id only accepting integers above 0 and below 213"""
        ids = [
            -1,
            'test',
            1.0,
            300
        ]
        for id in ids:
            url = self.url + str(id)
            r = self.app.get(url)
            self.assertEqual(r.status_code, 404)

    def test_columns_returned(self):
        """ensure the column names are as expected"""
        expected_columns = ['Name', 'Height Rank', 'Height (m)', 'Height (ft)', 'Prom. (ft)', 'OS Grid Reference', 'Longitude', 'Latitude']
        url = self.url + self.id
        r = self.app.get(url)
        json_data = json.loads(r.get_data())
        retrieved_columns = [col for col in json_data]
        self.check_lists_are_equal(expected_columns, retrieved_columns)


class FellsTest(Framework):
    """unittest for the fells/ endpoint"""

    def setUp(self):
        super().setUp()
        self.url = "/fells/"

    def test_returns_all_data_with_no_query(self):
        """ensures the entire database is returned if no query is made and all 214 fells are included"""
        r = self.app.get(self.url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        self.assertEqual(df.index.stop, 214)

    def test_returns_data_with_valid_single_name(self):
        """test fells data with single valid query"""
        query = self.generate_query(name=self.fell_name)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        self.assertGreater(df.index.stop,0)

    def test_returns_data_with_valid_multiple_names(self):
        """checks api returns multiple names with multiple name inputs"""
        query = '?name=scafell&name=skiddaw'
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        self.assertGreater(df.index.stop, 2)
    
    def test_returns_data_with_valid_multiple_queries(self):
        """test fells data with multiple queries"""
        query = self.generate_query(longitude=self.longitude, latitude=self.latitude)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        self.assertGreater(df.index.stop,0)

    def test_not_using_longlat_if_grid_reference_provided(self):
        """nearest fells should only be calculatd using grid if both grid and longlat provided"""
        query = self.generate_query(gridref=self.grid_reference)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        nearest = df.iloc[0]
        longitude = nearest['Longitude']
        latitude = nearest['Latitude']
        self.assertTrue(self.longitude != longitude)
        self.assertTrue(self.latitude != latitude)

    def test_uses_grid_reference_if_grid_reference_and_longlat_provided(self):
        """api uses grid reference if grid reference AND longitude and latitude provided"""
        query = self.generate_query(gridref=self.grid_reference, longitude=self.longitude, latitude=self.latitude)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        nearest = df.iloc[0]
        longitude = nearest['Longitude']
        latitude = nearest['Latitude']
        self.assertTrue(self.longitude != longitude)
        self.assertTrue(self.latitude != latitude)

    def test_uses_longlat_if_grid_reference_not_provided(self):
        """checks longitude and latitude is used if no grid reference is provided"""
        query = self.generate_query(longitude=self.longitude, latitude=self.latitude)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        nearest = df.iloc[0]
        self.assertEqual(nearest['Name'], 'Skiddaw')

    def test_does_not_filter_if_not_both_longlat_provided(self):
        """checks no filtering is carried out unless both longitude and latitude are provided"""
        query = self.generate_query(longitude=self.longitude)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)
        df = self.convert_request_to_df(r)
        self.assertEqual(df.index.stop, 214)

        query = self.generate_query(latitude=self.latitude)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)
        df = self.convert_request_to_df(r)
        self.assertEqual(df.index.stop, 214)

    def test_404_if_invalid_query(self):
        """returns 404 if invalid query is sent"""
        query = self.generate_query(name=self.fell_name).replace('?','')
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 404)

    def test_200_if_above_query_valid(self):
        """returns dataset if valid number if sent as 'above' variable"""
        query = self.generate_query(above=200)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        self.assertGreater(df.index.stop, 0)

    def test_404_if_above_query_is_not_valid_float(self):
        """returns 404 if invalid number is sent as 'above' variable"""
        invalid_numbers = [
            'hello',
        ]
        for invalid_number in invalid_numbers:
            query = self.generate_query(above=invalid_number)
            url = self.url + query
            r = self.app.get(url)
            self.assertIn(r.status_code, [404,500])

    def test_200_if_below_query_valid(self):
        """returns dataset if valid number if sent as 'below' variable"""
        query = self.generate_query(below=800)
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)

        df = self.convert_request_to_df(r)
        self.assertGreater(df.index.stop, 0)

    def test_404_if_below_query_is_not_valid_float(self):
        """returns 404 if invalid number is sent as 'below' variable"""
        invalid_numbers = [
            'hello',
        ]
        for invalid_number in invalid_numbers:
            query = self.generate_query(below=invalid_number)
            url = self.url + query
            r = self.app.get(url)
            self.assertIn(r.status_code, [404,500])

    def test_xss(self):
        """check basic xss protection"""
        query = self.generate_query(name='<script>alert(1);</script>')
        url = self.url + query
        r = self.app.get(url)
        self.assertEqual(r.status_code, 200)
    
    

