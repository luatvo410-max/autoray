import streamlit as st

st.title("AutoRAY 🚗")

# A small starter list—not a complete vehicle database.
cars = {
    "Toyota": ["Corolla", "Camry", "RAV4"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Infiniti": ["G37"],
    "Other / not listed": ["Other"],
}

# Remember progress and answers between questions.
if "page" not in st.session_state:
    st.session_state.page = 0
     #
if "answers" not in st.session_state:
    st.session_state.answers = {}

answers = st.session_state.answers
page = st.session_state.page


def ray(message):
    with st.chat_message("assistant", avatar="🤖"):
        st.write(message)


def navigation(updates):
    back, forward = st.columns(2)

    with back:
        if st.button("Back", disabled=page == 0):
            answers.update(updates)
            st.session_state.page -= 1
            st.rerun()

    with forward:
        label = "Show my results" if page == 4 else "Next"
        if st.button(label, type="primary"):
            answers.update(updates)
            st.session_state.page += 1
            st.rerun()


if page < 5:
    st.caption(f"Step {page + 1} of 6")
    st.progress(page / 5)

# STEP 1: Select the vehicle.
if page == 0:
    ray("Hey! I’m Ray. What car are you considering?")

    year_options = list(range(2027, 1989, -1))
    year = st.selectbox(
        "Year",
        year_options,
        index=year_options.index(answers.get("year", 2012)),
    )

    makes = list(cars)
    make = st.selectbox(
        "Make",
        makes,
        index=makes.index(answers.get("make", "Infiniti")),
    )

    models = cars[make]
    saved_model = answers.get("model")
    model = st.selectbox(
        "Model",
        models,
        index=models.index(saved_model) if saved_model in models else 0,
    )

    custom_car = ""
    if make == "Other / not listed":
        custom_car = st.text_input(
            "Enter your make and model",
            value=answers.get("custom_car", ""),
        )

    st.caption(
        "Starter list only. Model availability varies by year. "
        "Vehicle selection does not automatically set cost estimates yet."
    )

    navigation({
        "year": year,
        "make": make,
        "model": model,
        "custom_car": custom_car,
    })

# STEP 2: Purchase price.
elif page == 1:
    ray("What’s the asking price? You can use the price from a listing.")

    unsure = st.checkbox(
        "I don’t know the price yet",
        value=answers.get("unsure_price", False),
    )

    if unsure:
        st.info(
            "Use a planning amount below. The $20,000 starting value "
            "is a sample assumption, not a market valuation."
        )

    price = st.number_input(
        "Purchase price or planning amount ($)",
        min_value=0.0,
        value=float(answers.get("price", 20000.0)),
        step=500.0,
    )

    navigation({"price": price, "unsure_price": unsure})

# STEP 3: Driving habits.
elif page == 2:
    ray(
        "About how many miles do you drive per day? "
        "Include weekends when estimating your daily average."
    )

    miles = st.number_input(
        "Average miles per day",
        min_value=0.0,
        value=float(answers.get("miles", 30.0)),
        step=5.0,
    )

    st.caption(f"That’s approximately {miles * 365:,.0f} miles per year.")

    navigation({"miles": miles})

# STEP 4: Ownership length.
elif page == 3:
    ray("How many years do you plan to keep this car?")

    years = st.number_input(
        "Years of ownership",
        min_value=1,
        value=int(answers.get("years", 5)),
        step=1,
    )

    navigation({"years": years})

# STEP 5: Review assumptions.
elif page == 4:
    ray(
        "Let’s review the assumptions. Don’t know an amount? "
        "You can keep the sample value and adjust it later."
    )

    st.info(
        "These starting values are illustrative. They are not "
        "estimates specific to your selected car."
    )

    mpg = st.number_input(
        "Fuel economy (MPG)",
        min_value=1.0,
        value=float(answers.get("mpg", 25.0)),
        step=1.0,
        help="Use your car’s combined MPG or your observed average.",
    )

    gas_price = st.number_input(
        "Gas price ($ per gallon)",
        min_value=0.0,
        value=float(answers.get("gas_price", 4.50)),
        step=0.10,
    )

    annual_miles = answers["miles"] * 365
    annual_gas = annual_miles / mpg * gas_price

    st.write(f"Estimated yearly gas cost: **${annual_gas:,.2f}**")

    maintenance = st.number_input(
        "Maintenance and repair budget ($ per year)",
        min_value=0.0,
        value=float(answers.get("maintenance", 800.0)),
        step=100.0,
        help="A planning budget, not a prediction of repair bills.",
    )

    insurance = st.number_input(
        "Insurance ($ per month)",
        min_value=0.0,
        value=float(answers.get("insurance", 100.0)),
        step=10.0,
        help="Use an insurance quote if available.",
    )

    resale_percent = st.slider(
        "Expected resale value (% of purchase price)",
        min_value=0,
        max_value=100,
        value=int(answers.get("resale_percent", 40)),
        step=5,
        help="A planning assumption for the end of your ownership period.",
    )

    resale = answers["price"] * resale_percent / 100
    st.write(f"Expected resale amount: **${resale:,.2f}**")

    navigation({
        "mpg": mpg,
        "gas_price": gas_price,
        "maintenance": maintenance,
        "insurance": insurance,
        "resale_percent": resale_percent,
    })

# STEP 6: Results.
else:
    years = answers["years"]
    price = answers["price"]

    annual_miles = answers["miles"] * 365
    gas_total = (
        annual_miles / answers["mpg"]
        * answers["gas_price"] * years
    )
    maintenance_total = answers["maintenance"] * years
    insurance_total = answers["insurance"] * 12 * years
    resale = price * answers["resale_percent"] / 100

    total = (
        price + gas_total + maintenance_total
        + insurance_total - resale
    )

    if answers["make"] == "Other / not listed":
        car_name = answers["custom_car"] or "your car"
    else:
        car_name = f'{answers["make"]} {answers["model"]}'

    st.progress(1.0)

    ray(
        f'For your {answers["year"]} {car_name}, '
        f"the estimated ownership cost over {years} years "
        f"is ${total:,.0f}, after expected resale."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total cost", f"${total:,.0f}")
    col2.metric("Per year", f"${total / years:,.0f}")
    col3.metric("Per month", f"${total / years / 12:,.2f}")
    running_per_month = (
        gas_total + maintenance_total + insurance_total
    ) / years / 12

    ray(
        f"Your gas, maintenance, and insurance budget is about "
        f"${running_per_month:,.2f} per month. "
        "This excludes the purchase price and resale value."
    )

    with st.expander("View cost breakdown"):
        st.write(f"Purchase: ${price:,.2f}")
        st.write(f"Gas: ${gas_total:,.2f}")
        st.write(f"Maintenance and repairs: ${maintenance_total:,.2f}")
        st.write(f"Insurance: ${insurance_total:,.2f}")
        st.write(f"Minus expected resale: ${resale:,.2f}")
        st.write(f"Annual driving: {annual_miles:,.0f} miles")

    st.caption(
        "Based on your inputs and planning assumptions. "
        "Excludes financing, taxes, registration, and parking. "
        "Monthly cost is an average, not a loan payment."
    )

    edit_col, restart_col = st.columns(2)

    with edit_col:
        if st.button("Edit my answers"):
            st.session_state.page = 0
            st.rerun()

    with restart_col:
        if st.button("Start fresh"):
            st.session_state.answers = {}
            st.session_state.page = 0
            st.rerun()