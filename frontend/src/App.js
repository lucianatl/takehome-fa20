import React, { Component } from 'react'
import Instructions from './Instructions'
import Restaurant from './Restaurant'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      // this will hold the name of the inputted restaurant
      restaurantInput: '',
      // this is how many restaurants there are so far
      restaurantIdCount: 3,

      restaurants: [
        {id: 1, name: "Golden Harbor", rating: 10},
        {id: 2, name: "Potbelly", rating: 6},
        {id: 3, name: "Noodles and Company", rating: 8},
      ]
    }
  }

  InputRestaurant = () => { 
    this.setState((prevState) => ({
      restaurantIdCount: prevState.restaurantIdCount + 1
    }), () => {
      // this is creating the newly inputted restaurant
      let newRestaurant = {id: this.state.restaurantIdCount, name: this.state.restaurantInput, rating: 0};

      //this will add the new restaurant into our restaurants
      this.setState((prevState) => ({
          restaurants: [...prevState.restaurants, newRestaurant]
      }));
    }); 
  }

  // this will set the restaurant input variable equal to the inputted name of the new restuarant
  updateRestaurantInputValue(evt) {
    this.setState({
      restaurantInput: evt.target.value
    });
  }
  render() {
    return (
      <div className="App">
      
        <Instructions complete={true} />

        {this.state.restaurants.map(x => (
          <Restaurant id={x.id} name={x.name} rating={x.rating} />
        ))}
          <div>
             <input value={this.state.inputValue} onChange={evt => this.updateRestaurantInputValue(evt)}/>

             <button type="button" onClick={this.InputRestaurant}>Add Restaurant</button>
          </div>
          
      </div>
    )
  }
}

export default App
