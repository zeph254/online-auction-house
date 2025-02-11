export default function Home() {
    return (
      <div className="container mt-5">
      <h1 className="text-center fw-bold">Welcome to AUCTIGON</h1>
      <p className="text-center text-muted">
          Bringing transparency, efficiency, and security to online auctions.
      </p>

      <div className="d-flex align-items-center bg-light shadow-sm p-3 mb-4 rounded">
          <img className="img-fluid rounded" 
               style={{ width: "30%" }} 
               src="https://images.pexels.com/photos/5668802/pexels-photo-5668802.jpeg?cs=srgb&dl=pexels-sora-shimazaki-5668802.jpg&fm=jpg" 
               alt="Auction Scene" />
          <p className="ms-3 flex-grow-1">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Veniam laudantium quo esse ullam tempora unde provident dolore dolorum sed sint voluptatum nam ad modi, labore enim eligendi eaque nobis ea.
          </p>
      </div>

      <div className="d-flex align-items-center bg-light shadow-sm p-3 mb-4 rounded">
          <img className="img-fluid rounded" 
               style={{ width: "30%" }} 
               src="https://media.gettyimages.com/id/182232549/photo/green-auction-enter-button.jpg?s=612x612&w=gi&k=20&c=asO-rXhYaNzmI49a4CKHlve77ux3NonpEfCeyjFDojo=" 
               alt="Auction Button" />
          <p className="ms-3 flex-grow-1">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Asperiores quisquam aliquam minima et perspiciatis impedit laboriosam architecto unde sint voluptatibus nisi libero facilis cupiditate fuga voluptate, quaerat neque reiciendis ducimus?
          </p>
      </div>

      <div className="d-flex align-items-center bg-light shadow-sm p-3 mb-4 rounded">
          <img className="img-fluid rounded" 
               style={{ width: "30%" }} 
               src="https://static.startuptalky.com/2022/05/online-auction-market-StartupTalky.jpg" 
               alt="Auction Market" />
          <p className="ms-3 flex-grow-1">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure cupiditate harum illum maxime, iste fugiat rerum ut repudiandae exercitationem odit, porro eius, perferendis distinctio voluptatem ullam maiores similique suscipit nam!
          </p>
      </div>
  </div>
    );
}